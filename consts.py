from enum import Enum

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Arkanoid"

class CollisionTypes(int, Enum):
    PLAYER = 0
    BALL = 1
    WALL = 2
    BRICK = 3

class ShapeTypes(int, Enum):
    SPHERE = 0
    LINE = 1
    RECTANGLE = 2

class BodyTypes(int, Enum):
    DYNAMIC = 0
    STATIC = 1
