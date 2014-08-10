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
from navbot import Navbot

class Arena(Entity):

    def __init__(self):

        # Initialize arena as an entity
        body = pygame.Rect(0, 0, 400, 400)
        Entity.__init__(self, "arena.png", body)

        # Initialize basic arena traits
        self.num_bots = 2
        self.walls = []
        arena_data = {"num_bots": self.num_bots,
                      "walls": self.walls,
                      "height": self.body.height,
                      "width": self.body.width}

        # Initialize real bots
        # For now, hardcode in two dumbbots for testing
        self.bots = pygame.sprite.LayeredUpdates()
        self.bots.add(Realbot(Dumbbot(arena_data), 10, 100))
        self.bots.add(Realbot(Dumbbot(arena_data), 200, 100))
        self.bots.add(Realbot(Navbot(arena_data), 250, 100))

        # Declare another list that stores non-bots
        self.others = pygame.sprite.LayeredUpdates()

    def remove_dead(self, sprite_group):
        rm_list = []
        for entity in sprite_group.sprites():
            if entity.is_dead(self):
                rm_list.append(entity)
        for entity in rm_list:
            sprite_group.remove(entity)

    """
    Called once per game tick
    Updates entities on the arena
    """
    def update(self, events, elapsed):

        # Do updates
        for bot in self.bots.sprites():
            bot.update(self, elapsed)
        for entity in self.others.sprites():
            entity.update(self, elapsed)

        # Remove dead stuff
        self.remove_dead(self.others)
        self.remove_dead(self.bots)


    """
    Called once per game frame
    Clears the arena and redraws the entities in updated positions
    Output: A list of rects that need to be redrawn
    """
    def draw(self, screen):
        screen.blit(self.baseImage, self.baseRect)
        self.bots.draw(screen)
        self.others.draw(screen)

        # For now, just hardcode the entire arena to be redrawn
        return [self.baseRect]
