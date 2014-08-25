"""
entity.py

An entity is a physical body in the arena. It is the base class for anything
from realbots to bullets.
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from utils.resource import load_image

class Entity(pygame.sprite.Sprite):

    """
    All entities have a size. This is defined class-wide and should be
    overridden.
    """
    SIZE = (0, 0)

    """
    Initialize the entity with an image and position
    """
    def __init__(self,
                 image_path = None,
                 body = pygame.Rect(0, 0, 0, 0),
                 direction = d.direction.RIGHT):

        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # Attach image, if given
        if image_path:
            self.base_image, self.base_rect = load_image(image_path)
            self.image = self.base_image
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
    Called by other entites to retrieve public information about this
    entity. Designed to be overridden by subclasses
    """
    def get_info(self):
        info = {}
        info["type"] = None
        return info

    """
    Utility function that centers physical and sprite positions
    """
    def center(self):
        self.rect = self.image.get_rect()
        offset_left = self.body.width/2 - self.rect.width/2
        offset_top = self.body.height/2 - self.rect.height/2
        self.rect.left = self.body.left + offset_left
        self.rect.top = self.body.top + offset_top

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
    def set_pos(self, left, top):
        self.body.left = left
        self.body.top = top
        self.center()

