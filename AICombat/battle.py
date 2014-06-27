"""
Battle.py

Responsible for all battle logic. Maintains the arena and a list of all bots
currently inside.
"""

# Global imports
import pygame

# Local imports
import resource
from arena import Arena

class Battle():

    def __init__(self):

        # Initialize arena
        self.arena = Arena()

        # Initialize other bookkeeping variables
        self.totalElapsed = 0

    """
    Called once per game loop iteration
    Updates all bot actions
    """
    def update(self, events, elapsed):
        self.arena.update(events, elapsed)
        self.totalElapsed += elapsed

    """
    Called once per game loop iteration
    Clears the arena and redraws the bots in updated positions
    """
    def draw(self, screen):
        self.arena.draw(screen)
