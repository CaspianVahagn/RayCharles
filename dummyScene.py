from PIL import Image
import datetime
from math import sqrt


# GEOMETRICS


# Primitives

class Vector(object):
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


    def len(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


    def normalized(self):
        len = self.len()
        return Vector(self.x / len, self.y / len, self.z / len)

    # Kreuzprodukt
    def cross(self, v2):
        return Vector(
            self.y * v2.z - self.z * v2.y,
            self.z * v2.x - self.x * v2.z,
            self.x * v2.y - self.y * v2.x
        )

    # skalarprodukt
    def dot(self, v2):
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    # spiegeln
    def reflect(self, axis):
        return self - 2 * (self.dot(axis)) * axis

    # scale
    def __mul__(self, t):
        return Vector(self.x * t, self.y * t, self.z * t)

    __rmul__ = __mul__

    # add
    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    __radd__ = __add__

    # subtract
    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    __rsub__ = __sub__

    # print self
    def __repr__(self):
        return "Vektor(x: %s, y :%s, z: %s)" % (self.x, self.y, self.z)

    # invert
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __truediv__(self, k):
        return Vector(self.x / k, self.y / k, self.z / k)


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()

    def __repr__(self):
        return "Ray(%s, % s)" % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center  # point
        self.radius = radius  # radius
        self.material = material

    def __repr__(self):
        return "Sphere(%s, %s)" % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v * v - co.dot(co) + self.radius * self.radius
        if discriminant < 0:
            return None
        else:
            return v - sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()


class Plane(object):
    def __init__(self, point, normal, material):
        self.point = point  # point
        self.normal = normal.normalized()  # vector
        self.material = material

    def __repr__(self):
        return "Plane(%s,%s)" % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a / b
        else:
            return None

    def normalAt(self, p):
        return self.normal


class Triangle(object):
    def __init__(self, a, b, c, material):
        self.a = a  # point
        self.b = b  # point
        self.c = c  # point
        self.material = material
        self.u = self.b - self.a
        self.v = self.c - self.a

    def __repr__(self):
        return "Triangle(%s,%s,%s)" % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0 <= r <= 1 and 0 <= s <= 1 and r + s <= 1:
            return wu.dot(self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()


# SCENE OBJECTS

class Camera(object):
    def __init__(self, eye, focalpoint, up):
        self.origin = eye
        self.focalpoint = focalpoint
        self.up = up
        # calcparams
        self.f = (focalpoint - eye).normalized()
        self.s = self.f.cross(up).normalized()
        self.u = self.s.cross(self.f)

    def __repr__(self):
        return "e: %s, c: %s, up: %s, f: %s, s: %s, u: %s" % (
            self.origin, self.focalpoint, self.up, self.f, self.s, self.u)


class Color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def toRGB(self):
        self.r = 255 if self.r > 255 else self.r
        self.g = 255 if self.g > 255 else self.g
        self.b = 255 if self.b > 255 else self.b

        self.r = 0 if self.r < 0 else self.r
        self.g = 0 if self.g < 0 else self.g
        self.b = 0 if self.b < 0 else self.b

        return int(self.r), int(self.g), int(self.b)

    def __mul__(self, k):
        return Color(self.r * k, self.g * k, self.b * k)

    __rmul__ = __mul__

    def __add__(self, k):
        return Color(self.r + k.r, self.g + k.g, self.b + k.b)

    def __repr__(self):
        return "Color(R %s G%s B%s)" % (self.r, self.g, self.b)


class Material(object):
    def __init__(self, diffuse, leveldiffuse, specular, levelspecular, ambient, levelambient, reflectivity=0):
        self.diffuse = diffuse
        self.leveldiffuse = leveldiffuse
        self.levelspecular = levelspecular
        self.specular = specular
        self.ambient = ambient
        self.levelambient = levelambient
        self.reflectivity = reflectivity

    def totalColor(self, diffMulti, specMulti):

        diffuse = self.diffuse * diffMulti * self.leveldiffuse
        specular = self.specular * specMulti * self.levelspecular

        if (diffuse.r < 0) | (diffuse.g < 0) | (diffuse.b < 0):
            diffuse = Color(0, 0, 0)
        if (specular.r < 0) | (specular.g < 0) | (specular.b < 0):
            specular = Color(0, 0, 0)

        return diffuse * diffMulti * self.leveldiffuse + specular * specMulti * self.levelspecular + self.ambient * self.levelambient


class CheckerboardMaterial(object):
    def __init__(self, color, color2, checksize, leveldiffuse, specular, levelspecular, ambient, levelambient,
                 reflectivity=0):
        self.color = color
        self.color2 = color2
        self.checksize = checksize
        self.leveldiffuse = leveldiffuse
        self.levelspecular = levelspecular
        self.specular = specular
        self.ambient = ambient
        self.levelambient = levelambient
        self.reflectivity = reflectivity

    def colorAt(self, point, diffMulti, specMulti):
        point *= (1.0 / self.checksize)

        # if (int(sqrt(point.x ** 2) + 0.5) + int(sqrt(point.y ** 2) + 0.5) + int(sqrt(point.z ** 2) + 0.5)) % 2:
        #     return self.color2 * diffMulti * self.leveldiffuse + self.specular * specMulti * self.levelspecular + self.ambient * self.levelambient
        # return self.color * diffMulti * self.leveldiffuse + self.specular * specMulti * self.levelspecular + self.ambient * self.levelambient

        if (int(sqrt(point.x ** 2) + 0.5) + int(sqrt(point.y ** 2) + 0.5) + int(sqrt(point.z ** 2) + 0.5)) % 2:
            diffuse = self.color2 * diffMulti * self.leveldiffuse
        else:
            diffuse = self.color * diffMulti * self.leveldiffuse

        specular = self.specular * specMulti * self.levelspecular

        if (diffuse.r < 0) | (diffuse.g < 0) | (diffuse.b < 0):
            diffuse = Color(0, 0, 0)
        if (specular.r < 0) | (specular.g < 0) | (specular.b < 0):
            specular = Color(0, 0, 0)

        return diffuse * diffMulti * self.leveldiffuse + specular * specMulti * self.levelspecular + self.ambient * self.levelambient


class Light(object):
    def __init__(self, origin, intensity):
        self.origin = origin
        self.intensity = intensity


class Scene(object):
    def __init__(self):
        self.objects = []
        self.camera = None

    def setCamera(self, camera):
        self.camera = camera

    def appendObject(self, obj):
        self.objects.append(obj)


class Picture(object):
    def __init__(self, width, height, scene, light, camera, background=Color(0, 0, 0), depthmap=False, reflection=1):
        self.width = width
        self.height = height
        self.aspect = width / height
        self.scene = scene
        self.light = light
        self.camera = camera
        self.background = background
        self.image = Image.new("RGB", (width, height))
        if depthmap:
            self.depth = Image.new("RGB", (width, height))
        else:
            self.depth = False
        self.reflection = reflection
        self.viewGrid = (width, height)
        self.pixelWidth = self.viewGrid[0] / (self.width - 1)
        self.pixelHeight = self.viewGrid[1] / (self.height - 1)

    def render(self):
        self.castRays()
        if self.depth:
            self.depth.save("test" + datetime.datetime.now().strftime("%Y_%m_%H_%M") + ".jpg", "JPEG",
                            quality=90)
        self.image.save("test" + datetime.datetime.now().strftime("%Y_%m_%H_%M") + ".jpg", "JPEG",
                        quality=90)

    def calcRay(self, x, y):
        xcomp = self.camera.s * (x * self.pixelWidth - self.width / 2)
        ycomp = self.camera.u * (y * self.pixelHeight - self.height / 2)
        return Ray(self.camera.origin, self.camera.focalpoint + xcomp + ycomp)

    # ------________--------______-------_______------_______-------_______------________-----________------_____---------

    # diffuse + specular + ambient
    def computeDirectLight(self, distance, object, ray):
        diffMulti = 0
        specMulti = 0
        light = self.light

        schnittpunkt = ray.origin + distance * ray.direction
        n = object.normalAt(schnittpunkt)

        l = (light.origin - schnittpunkt).normalized()
        lr = l.reflect(n)

        diffMulti += l.dot(n) * light.intensity
        lrval = lr.dot(ray.direction.normalized())
        specMulti += lrval * light.intensity

        #for element in self.scene:
        #    if element.intersectionParameter(Ray(schnittpunkt, l)) is not None and element.intersectionParameter(
        #            Ray(schnittpunkt, l)) > 0.01:
        #        diffMulti *= 0
        #        specMulti *= 0
        #        break

        if hasattr(object.material, 'checksize'):
            return object.material.colorAt(schnittpunkt, diffMulti, specMulti)
        return object.material.totalColor(diffMulti, specMulti)

    # reflect viewing angle
    def computeReflectedRay(self, distance, object, ray):
        schnittpunkt = ray.origin + distance * ray.direction
        normal = object.normalAt(ray.origin + distance * ray.direction)
        return Ray(schnittpunkt, ray.direction.reflect(normal).normalized())

    # calculate reflection + light
    def shade(self, level, distance, object, ray):
        directColor = self.computeDirectLight(distance, object, ray)
        reflectedRay = self.computeReflectedRay(distance, object, ray)
        reflectedColor = self.traceRay(level + 1, reflectedRay)
        # refractedRay = computeRefractedRay(hitPointData) #refractColor = traceRay(level+1, refractedRay)

        return directColor + self.reflection * reflectedColor

    # follow ray direction
    def traceRay(self, level, ray):
        hitPointData = self.intersect(level, ray, 6)
        if hitPointData is not None:
            return self.shade(level, hitPointData[0], hitPointData[1], hitPointData[2])
        else:
            return Color(0, 0, 0)

    # check for collision
    def intersect(self, level, ray, maxlevel=1):
        if level > maxlevel:
            return None
        obj = None
        maxdist = float('inf')
        for object in self.scene:
            hitdist = object.intersectionParameter(ray)
            if hitdist and 0.01 < hitdist < maxdist:
                maxdist = hitdist
                obj = object
        if obj is None:
            return None
        return maxdist, obj, ray

    def castRays(self):
        depthColor = Color(255, 255, 255)
        maxdepth = 200
        for x in range(self.width):
            for y in range(self.height):
                color = self.background

                ray = self.calcRay(x, y)
                maxdist = self.intersect(1, ray)
                if maxdist is not None:
                    color = self.traceRay(1, ray)

                self.image.putpixel((x, y), color.toRGB())

                if self.depth and maxdist <= maxdepth:
                    self.depth.putpixel((x, y), (depthColor * (1 - maxdist / maxdepth)).toRGB())

        self.image.show()
