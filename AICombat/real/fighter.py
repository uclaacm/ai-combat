"""
fighter.py

A fighter is anything that conducts combat in the arena. Generally, a fighter:
1. Deals damage and/or
2. Takes damage
This includes bots, bullets, and possibly other entities in the future. This
class is a base class for all of them.
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from real.entity import Entity

class Fighter(Entity):

    """
    Initialize the fighter with an image, position, and hp
    """
    def __init__(self,
                 image_path = None,
                 body = pygame.Rect(0, 0, 0, 0),
                 direction = d.direction.RIGHT,
                 hp = 1):

        # Call Entity initializer
        Entity.__init__(self, image_path, body, direction)

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

    """
    Override of Entity's get_info() to provide public information about the
    fighter
    """
    def get_info(self):

        info = Entity.get_info(self)

        # Fighter information
        fighter_info = {"hp": self.hp}
        info.update(fighter_info)

        return info
