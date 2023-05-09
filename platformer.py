from enum import Enum, auto
import pygame
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
        self.motion = pygame.math.Vector2()
        self.air_frames = 0
        self.last_dir = Direction.RIGHT
        self.animations = AnimationManager()
        self.surf = None
        self.rect = None

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
        self.surf = self.animations.next(name)
        if not self.rect:
            self.rect = self.surf.get_rect()

    @property
    def surf_to_blit(self):
        '''
        Return a flipped version of the surf if facing left
        '''
        if self.last_dir == Direction.LEFT:
            return pygame.transform.flip(self.surf.copy(), True, False)

        return self.surf

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, val):
        self.rect.y = val
        
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

def collides_with_rects(src_rect, rects):
    '''
    Detects if src_rect collides with a list of rects

    Arguments:
        src_rect: pygame.Rect       The rect we want to test collision
        rects: List[pygame.Rect]    The rects we test against

    Return:
        pygame.Rect, None           The collided rect from rects
    '''
    for rect in rects:
        if src_rect.colliderect(rect):
            return rect

    return None

class Camera:
    '''
    Follow the target's movement. Meant for modiifying blit logic.
    The properties int_x and int_y are used for tracking relative
    updates to other objects relative to the target (like tiles)
    '''
    def __init__(self, target, width, height, follow_x=True, follow_y=True, follow_buffer=20):
        self.target = target
        self.width = width
        self.height = height
        self.pos = pygame.math.Vector2()
        self.pos.x += (target.x - self.pos.x - width // 2)
        self.pos.y += (target.y - self.pos.y - height // 2) 
        self.follow_x = follow_x
        self.follow_y = follow_y

        # We will divide by the follow buffer in update method
        if follow_buffer is None or follow_buffer == 0:
            follow_buffer = 1
        self.follow_buffer = follow_buffer

    @property
    def int_x(self):
        return int(self.pos.x)

    @property
    def int_y(self):
        return int(self.pos.y)

    def update(self):
        if self.follow_x:
            self.pos.x += (self.target.x - self.pos.x - self.width // 2) / self.follow_buffer
        if self.follow_y:
            self.pos.y += (self.target.y - self.pos.y - self.height // 2) / self.follow_buffer

    def __repr__(self):
        return f'Camera({self.pos.x}, {self.pos.y})'
