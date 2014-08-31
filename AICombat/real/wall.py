"""
wall.py

"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from real.entity import Entity

class Wall(Entity):

    """
    Initialize the wall
    """
    def __init__(self, body):

        # Call Entity initializer
        Entity.__init__(self, None, body, d.direction.RIGHT)

        # Manually generate image (just a black rectangle for now)
        self.image = pygame.Surface((body.width, body.height))
        self.image.fill(0)
        self.rect = self.body

