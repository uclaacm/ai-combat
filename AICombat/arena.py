"""
arena.py

Maintains the list of bots and other objects.
"""

# Global imports
import pygame

# Local imports
import resource
from entity import Entity
from realbot import Realbot
from dumbbot import Dumbbot

class Arena(Entity):

    def __init__(self):

        # Initialize arena as an entity
        body = pygame.Rect(0, 0, 400, 400)
        Entity.__init__(self, "arena.png", body)

        # Initialize real bots
        # For now, hardcode in two dumbbots for testing
        self.bots = pygame.sprite.LayeredUpdates()
        self.bots.add(Realbot(Dumbbot(), 10, 10))
        self.bots.add(Realbot(Dumbbot(), 200, 100))

        # Declare another list that stores non-bots
        self.others = pygame.sprite.LayeredUpdates()

    """
    Called once per game loop iteration
    Updates entities on the arena
    """
    def update(self, events, elapsed):
    
        # Do updates
        for bot in self.bots.sprites():
            bot.update(self, elapsed)
        for entity in self.others.sprites():
            entity.update(self, elapsed)

        # Remove dead stuff
        rm_list = []
        for entity in self.others.sprites():
            if entity.is_dead(self):
                rm_list.append(entity)
        for entity in rm_list:
            self.others.remove(entity)


    """
    Called once per game loop iteration
    Clears the arena and redraws the entities in updated positions
    """
    def draw(self, screen):
        screen.blit(self.baseImage, self.baseRect)
        self.bots.draw(screen)
        self.others.draw(screen)
