import pygame

QUIT_SCENE = pygame.USEREVENT + 1
MENU_MOVE_SOUND = pygame.USEREVENT + 2

def emit(event):
    '''
    Wrapper around posting pygame events
    '''
    pygame.event.post(pygame.event.Event(event))

