from enum import Enum, auto
from pygame.math import Vector2
from collections import defaultdict
from itertools import repeat, cycle, chain

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
        self.last_dir = Direction.RIGHT
        self.animations = AnimationManager()

        self.speed = speed
        self.gravity = gravity
        self.jump_force = jump_force
        self.max_fall_speed = max_fall_speed

    def update_vertical_movement(self):
        self.motion.y = min(self.max_fall_speed, self.motion.y + self.gravity)
        self.moving.down = self.motion.y > 0
        self.moving.up = self.motion.y <= 0

    @property
    def is_falling(self):
        '''
        An actor is falling when its vertical speed is greater
        than its gravity. This is because we set the vertical
        speed to its velocity when colliding with tiles below
        it. We want to make sure we don't do falling logic 
        while the actor is actually on the ground.
        '''
        return self.motion.y > self.gravity

    def animate(self, name):
        return self.animations.next(name)
        
class AnimationManager:
    def __init__(self, frame_scale=5):
        self.animation_dict = defaultdict(dict)
        self.frame_scale = frame_scale
        self.name = None

    @property
    def surfs(self):
        return self.animation_dict[self.name]['surfs']

    @surfs.setter
    def surfs(self, surfs):
        self.animation_dict[self.name]['surfs'] = surfs

    @property
    def cycle(self):
        return self.animation_dict[self.name]['cycle']

    @cycle.setter
    def cycle(self, cycle):
        self.animation_dict[self.name]['cycle'] = cycle
        
    def add_animation(self, name, surfs):
        '''
        Sets the surfs and cycle for an animation name
        '''
        total_frames = len(surfs) 
        self.animation_dict[name]['surfs'] = surfs
        scaled_frames = (repeat(idx, self.frame_scale) for idx in range(total_frames))
        self.animation_dict[name]['cycle'] = cycle(chain.from_iterable(scaled_frames))

    def __setitem__(self, key, value):
        '''
        Convenient way to use add_animation by key:value
        '''
        self.add_animation(key, value)

    def __getitem__(self, key):
        '''
        Gets the surfs for an animation name
        '''
        return self.animation_dict[key]['surfs']

    def next(self, name=None):
        '''
        Gets the next surf for current animation name
        '''
        if name:
            self.name = name
        return self.surfs[next(self.cycle)]
