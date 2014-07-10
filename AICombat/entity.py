"""
entity.py

An entity is a physical body in the arena. It is the base class for anything
from realbots to bullets.
"""

# Global imports
import pygame

# Local imports
import definitions as D
import resource

class Entity(pygame.sprite.Sprite):

    """
    Initialize the entity with an image and position
    """
    def __init__(self,
                 imagePath = None,
                 body = pygame.Rect(0,0,0,0),
                 direction = D.direction.RIGHT):

        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # Attach image, if given
        if imagePath:
            self.baseImage, self.baseRect = resource.loadImage(imagePath)
            self.image = self.baseImage
            self.rect = self.image.get_rect()

        # Set physical position, size, and direction
        # Note that physical size is not the same as sprite size
        # they're both centered on the same point, but the physical
        # size is the one used for ingame collision
        # (body is the physical, rect is the sprite)
        self.body = body
        self.direction = direction
        self.center()

    """
    Called once per game loop iteration
    A basic entity does nothing
    """
    def update(self, arena, elapsed):
        pass

    """
    Called by arena to see if entity can be safely removed
    A basic entity is immortal
    """
    def is_dead(self, arena):
        return False

    """
    Utility function that centers physical and sprite positions
    """
    def center(self):
        self.rect = self.image.get_rect()
        offsetLeft = self.body.width/2 - self.rect.width/2
        offsetTop = self.body.height/2 - self.rect.height/2
        self.rect.left = self.body.left + offsetLeft
        self.rect.top = self.body.top + offsetTop

    """
    Utility function to translate position
    """
    def move(self, x=0, y=0):
        self.rect.top += y
        self.rect.left += x
        self.body.top += y
        self.body.left += x

    """
    Utility function to change position
    """
    def setPos(self, left, top):
        self.body.left = left
        self.body.top = top
        self.center()

