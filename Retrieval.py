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