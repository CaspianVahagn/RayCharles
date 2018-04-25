from Rays import Ray
import math


class Sphere(object):

    def __init__(self, center, radius):
        self.center = center  # point
        self.radius = radius  # scalar

    def __repr__(self):
        return 'Sphere(%s%s)' % (repr(self.center), self.radius)


    def intersectionParameter(self, ray):
        co = self.center -ray.origin
        v = co.dot
        discriminant = v*v -co.dot(co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.squrt(discriminant)


    def normalAt(self, p):
        return (p - self.center).normalized()


class Plane(object):

    def __init__(self, point, normal):
        self.point = point
        self.normal = normal.normalized()

    def __repr__(self):
        return 'Plane(%s%s)' %(repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin -self.point
        a = op.dot(self.normal)
        b = ray.direction.dot()
        if b:
            return -a/b
        else:
            return None

    def normalAt(self, p):
        return self.normal

    def colorAt(self,p):
        return '#FFFFFF'

class Triangle(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.u = self.b -self.a # direction Vector
        self.v = self.c -self.a # direction Vector

    def __repr__(self):
        return 'Trangle(%s%s&s)' %(repr(self.a), repr(self.b),repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a

        dv= ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross (self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction)/ dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return wu.dot(self.v) /dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()