"""
bullet.py

A basic bullet shot from a gun that all realbots have
"""

# Global imports
import pygame

# Local imports
from definitions import *
import resource
from entity import Entity

class Bullet(Entity):

    def __init__(self, origin, direction, left, top):

        # Call Entity init
        body = pygame.Rect(left, top, 5, 5)
        Entity.__init__(self, "bullet.png", body, direction)
        self.center()

        # Other bookkeeping variables
        self.vel = 4
        self.origin = origin

    """
    A bullet is dead if it goes out of screen
    """
    def is_dead(self, arena):
        if not arena.body.colliderect(self.body):
            return True
        return False

    """
    Called once per game loop iteration
    """
    def update(self, arena, elapsed):
        self.move(self.vel*DC[self.direction], self.vel*DR[self.direction])
