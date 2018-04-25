from Rays import Ray
from Things import Plane,Sphere,Triangle
import numpy as np
import cv2

BACKGROUND_COLOR = "#000000"
objectlist = []
image = cv2.imwrite("rayt.jpg", np.asarray([]))
# image Params
width = 400
height = 400
# Kamera

e = np.asarray([0, 1.8, 10])
c = np.asarray([0, 3, 0])
up = np.asarray([0, 1, 0])
fov = 45




def calcRay(x,y):
    return Ray(e, np.asarray([x,y]))


def castRay (imageWidth, imageHeight):
    for x in range(imageWidth):
        for y in range(imageHeight):
            ray = calcRay(x,y)
            maxdist = float('inf')
            color = BACKGROUND_COLOR
            for object in objectlist:
                hitdist = object.intersectionParameters(ray)
                if hitdist:
                    if hitdist < maxdist:
                        maxdist = hitdist
                        color = object.colorAt(ray)
            image.putpixel((x, y), color)



if __name__ == '__main__':
    objectlist.append(Plane(np.asarray([34,22]),np.asarray([34,22])))
    castRay(width,height)

