"""
Battle.py

Responsible for all battle logic. Maintains the arena object
"""

# Global imports
import pygame

# Local imports
from arena import Arena

class Battle():

    def __init__(self):

        # Initialize arena
        self.arena = Arena()

        # Initialize other bookkeeping variables
        self.totalElapsed = 0

    """
    Called once per game loop iteration
    Updates arena
    """
    def update(self, events, elapsed):
        self.arena.update(events, elapsed)
        self.totalElapsed += elapsed

    """
    Called once per game loop iteration
    Draws the arena
    """
    def draw(self, screen):
        self.arena.draw(screen)
