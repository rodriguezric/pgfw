import pygame

class KeyHandler:
    '''                                                     
    Binds a function to itself to handle pygame events. It  
    skips all events that are not KEYDOWN. The bound fn is
    expected to have an event parm and potentially kwargs.
    '''
    def __init__(self, callback):
        method = callback.__get__(self, self.__class__)
        self.callback = method

    def __call__(self, event, **kwargs):
        if event.type != pygame.KEYDOWN:                    
            return
        else:
            self.callback(event, **kwargs)

def key_handler(fn):
    '''
    Decorator to save making a function and then instantiating
    a class repeatedly
    '''
    return KeyHandler(fn)

