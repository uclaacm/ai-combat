"""
resource.py

Taken from http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
Contains utility resource loading functions
"""

import pygame
import os

def loadImage(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def loadSound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound
