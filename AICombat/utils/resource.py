"""
resource.py

Taken from http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
Contains utility resource loading functions
"""

import pygame

"""
Loads an image
IN:  - string representing path to image
     - optional pygame.Color specifying the colorkey for the image, which
       determines what color should be transparent
OUT: - pygame.Surface of the image
     - pygame.Rect of the image
"""
def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

"""
Loads a sound file
IN:  - string representing path to sound file
OUT: - pygame.mixer.Sound object representing the waveform
"""
def load_sound(name):
    class NoneSound(object):
        def play(self):
            pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error as message:
        print 'Cannot load sound:', name
        raise SystemExit(message)
    return sound
