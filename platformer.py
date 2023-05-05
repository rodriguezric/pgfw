from enum import Enum, auto
from pygame.math import Vector2

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Moving:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def __bool__(self):
        return any((self.up, self.down, self.left, self.right))

    @property
    def vertical(self):
        return self.up or self.down

    @property
    def horizontal(self):
        return self.right or self.left

class Actor:
    def __init__(self, speed, gravity, jump_force, max_fall_speed):
        self.moving = Moving()
        self.motion = Vector2()
        self.air_frames = 0

        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.max_fall_speed = max_fall_speed
