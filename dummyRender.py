import dummyScene as scene

Vector = scene.Vector

# Colors
red = scene.Color(255, 0, 0)
green = scene.Color(0, 255, 0)
blue = scene.Color(0, 0, 255)
yellow = scene.Color(255, 255, 0)
white = scene.Color(255, 255, 255)
grey = scene.Color(128, 128, 128)
darkgrey = scene.Color(20, 20, 20)
black = scene.Color(0, 0, 0)

# Materials
defaultMaterial = scene.Material(grey, 0.3, grey * 1.6, 0.7, grey, 0.1)
redMaterial = scene.Material(red, 0.3, red + grey, 0.7, grey, 0.1)
greenMaterial = scene.Material(green, 0.3, green + grey, 0.7, grey, 0.1)
blueMaterial = scene.Material(blue, 0.3, blue + grey, 0.7, grey, 0.1)
yellowMaterial = scene.Material(yellow, 0.3, yellow + grey, 0.7, grey, 0.1)
blackMaterial = scene.Material(black, 0.3, black, 0.7, grey, 0)
checkersMaterial = scene.CheckerboardMaterial(black, white, 4.0, 0.3, white, 0.7, grey, 0.1)

# Scene Objects
SCENE_LIGHT = scene.Light(Vector(-100, 100, -40), 1)

SCENE_OBJECTS = [
    scene.Plane(Vector(0, -50, 200), Vector(0, 1, 0), defaultMaterial),
    scene.Sphere(Vector(30, 0, 100), 20, redMaterial),
    scene.Sphere(Vector(-30, 0, 100), 20, greenMaterial),
    scene.Sphere(Vector(0, 45, 100), 20, blueMaterial),
    scene.Triangle(Vector(0, 45, 100), Vector(30, 0, 100), Vector(-30, 0, 100), yellowMaterial),
]

CAMERA = scene.Camera(
    Vector(0, -5, 0),  # origin
    Vector(0, 45, 250),  # focalpoint
    Vector(0, -1, 0)  # up
)

# Image
picture = scene.Picture(600, 600, SCENE_OBJECTS, SCENE_LIGHT, CAMERA, background=black, depthmap=False, reflection=1)

if __name__ == "__main__":
    picture.render()