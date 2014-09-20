"""
Battle.py

Responsible for all battle logic. Maintains the arena object
"""

# Local imports
from arena import Arena

class Battle(object):

    def __init__(self):

        # Initialize arena
        self.arena = Arena()

        # Initialize other bookkeeping variables
        self.total_elapsed = 0

    """
    Called once per game tick
    Updates arena
    """
    def update(self, events, elapsed):
        self.arena.update(events, elapsed)
        self.total_elapsed += elapsed

    """
    Called once per frame
    Draws the arena
    """
    def draw(self, screen):
        return self.arena.draw(screen)
