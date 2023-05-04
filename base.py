import pygame
import sys

def quit_game():
    pygame.quit()
    sys.exit()

TILE_SIZE = 16     
WIDTH = 512
HEIGHT = 512

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

font = pygame.font.Font('fonts/prstart.ttf', TILE_SIZE) 

