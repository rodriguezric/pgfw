import dataclasses
import pygame
import glob

from framework.base import *
from framework.event import MENU_MOVE_SOUND
from framework.event import emit

font = pygame.font.Font('fonts/prstart.ttf', TILE_SIZE)

class Window:
    '''
    Class for conveniently creating two pygame Rects: background and border
    Meant for combining with a list of text to create a menu or popup
    '''
    def __init__(self, width, height, border_color='white', fill_color='black', x=0, y=0, **dump):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.update_border_rect()
        self.border_color = border_color
        self.fill_color = fill_color

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

    @property
    def pos(self):
        return (self.rect.x, self.rect.y)

    @pos.setter
    def pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_border_rect(self):
        self.border_rect = self.rect.copy()
        self.border_rect.x = 0
        self.border_rect.y = 0

    def draw(self):
        self.surf.fill(self.fill_color)
        pygame.draw.rect(self.surf, self.border_color, self.border_rect, 1)

@dataclasses.dataclass
class Padding:
    bottom : int = 0
    left : int = 0
    right : int = 0
    top : int = 0

class TextLines:
    '''
    Class for drawing several lines of text
    '''
    def __init__(self, target_surf, text_lines, color='white', padding=Padding(), spacing=0, x=0, y=0):
        self.target_surf = target_surf
        self.text_lines = text_lines
        self.color = color
        self.padding = padding
        self.spacing = spacing
        self.x = x
        self.y = y

    def draw(self):
        for line, text in enumerate(self.text_lines):
            surf = font.render(text, False, self.color)
            pos = (self.x + self.padding.left,
                   self.y + self.padding.top + line * (TILE_SIZE + self.spacing))
            self.target_surf.blit(surf, pos)

class Cursor:
    def __init__(self, target_surf, rows, color='white', padding=Padding(), spacing=0, x=0, y=0):
        self.surf = font.render('>', False, color)
        self.rect = self.surf.get_rect()
        self.rect.x = x + padding.left
        self.idx = 0

        self.y = y
        self.target_surf = target_surf
        self.rows = rows
        self.color = color
        self.padding = padding
        self.spacing = spacing
        self.update_rect()
        self.draw()

    def update_rect(self):
        self.rect.y = self.y + self.padding.top + self.idx * (TILE_SIZE + self.spacing)

    def move_up(self):
        prev = self.idx
        self.idx = max(self.idx - 1, 0)
        if self.idx != prev:
            emit(MENU_MOVE_SOUND)
        self.update_rect()

    def move_down(self):
        prev = self.idx
        self.idx = min(self.idx + 1, self.rows - 1)
        if self.idx != prev:
            emit(MENU_MOVE_SOUND)
        self.update_rect()

    def draw(self):
        self.target_surf.blit(self.surf, self.rect)

class Menu:
    def __init__(self, width, height, text_lines, **kwargs):
        cursor_padding = kwargs.pop('padding', Padding(left=TILE_SIZE))
        text_padding = dataclasses.replace(cursor_padding)
        text_padding.left += TILE_SIZE

        fill_color = kwargs.pop('fill_color', 'black')
        border_color = kwargs.pop('border_color', 'white')

        self.window = Window(width, height, fill_color=fill_color, border_color=border_color, **kwargs)
        self.text_lines = TextLines(self.window.surf, text_lines=text_lines, padding=text_padding, **kwargs)
        self.cursor = Cursor(self.window.surf, rows=len(text_lines), padding=cursor_padding, **kwargs)

        self.surf = self.window.surf
        self.rect = self.window.rect

    def move_up(self):
        self.cursor.move_up()

    def move_down(self):
        self.cursor.move_down()

    def draw(self):
        self.window.draw()
        self.text_lines.draw()
        self.cursor.draw()

    @property
    def idx(self):
        return self.cursor.idx

class TextWindow(Window):
    def __init__(self, width, height, text_lines, **kwargs):
        super().__init__(width, height, **kwargs)
        self.text_lines = TextLines(self.surf, text_lines=text_lines, **kwargs)

    def draw(self):
        super().draw()
        self.text_lines.draw()

def popup_menu(text_lines):
    '''
    Helper function for creating quick, centered popup menus
    '''
    menu = Menu(
        width=TILE_SIZE * 12,
        height=TILE_SIZE * (len(text_lines) + 1),
        text_lines=text_lines,
        padding=Padding(top=TILE_SIZE//2),
    )
    menu.rect.center = screen_rect.center

    return menu

def scale_surf(scale_tuple):
    def inner(surf):
        return pygame.transform.scale(surf, scale_tuple)
    return inner

def get_surfs(path):
    files = reversed(glob.glob(path))
    return map(pygame.image.load, files)

def get_scaled_surfs(path, scale_tuple):
    return list(map(scale_surf(scale_tuple), get_surfs(path)))

