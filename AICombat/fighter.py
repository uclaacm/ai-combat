"""
fighter.py

A fighter is anything that conducts combat in the arena. Generally, a fighter:
1. Deals damage and/or
2. Takes damage
This includes bots, bullets, and possibly other entities in the future
"""

# Global imports
import pygame

# Local imports
import definitions as d
from entity import Entity

class Fighter(Entity):

    """
    Initialize the fighter with an image, position, and hp
    """
    def __init__(self,
                 imagePath = None,
                 body = pygame.Rect(0,0,0,0),
                 direction = d.direction.RIGHT,
                 hp = 1):

        # Call Entity initializer
        Entity.__init__(self, imagePath, body, direction)

        # Initialize fighter attributes
        self.hp = hp

    """
    Most of the time a fighter is dead when its hp is 0, although subclasses
    can override this behavior
    """
    def is_dead(self, arena):
        return self.hp <= 0

    """
    Called when the fighter is struck 
    """
    def hit(self, dmg):
        self.hp -= dmg

