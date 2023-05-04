import pygame

QUIT_SCENE = pygame.USEREVENT + 1

def emit(event):
    '''
    Wrapper around posting pygame events
    '''
    pygame.event.post(pygame.event.Event(event))

