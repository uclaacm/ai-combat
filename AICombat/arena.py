"""
arena.py

Maintains the list of bots and other objects.
"""

# Global imports
import pygame

# Local imports
import utils.geometry
from real.realbot import Realbot
from real.entity import Entity
from real.wall import Wall
from virtual import *

class Arena(Entity):

    def __init__(self):

        # Initialize arena as an entity
        body = pygame.Rect(0, 0, 400, 400)
        Entity.__init__(self, "img/arena.png", body)

        # Initialize basic arena traits
        # For now, hardcode some walls for testing
        self.num_bots = 2
        self.walls = pygame.sprite.LayeredUpdates()
        self.walls.add(Wall(pygame.Rect(100, 100, 100, 10)))
        self.walls.add(Wall(pygame.Rect(100, 200, 52, 148)))
        self.walls.add(Wall(pygame.Rect(0, 30, 100, 10)))
        self.walls.add(Wall(pygame.Rect(40, 100, 12, 96)))
        self.walls.add(Wall(pygame.Rect(60, 150, 6, 86)))
        self.walls.add(Wall(pygame.Rect(200, 0, 20, 96)))
        arena_data = {"num_bots": self.num_bots,
                      "walls": self.walls.sprites(),
                      "height": self.body.height,
                      "width": self.body.width}

        # Initialize real bots
        # For now, hardcode in bots for testing
        self.bots = pygame.sprite.LayeredUpdates()
        self.bots.add(Realbot(dumbbot.Dumbbot(arena_data), self, 10, 100))
        self.bots.add(Realbot(dumbbot.Dumbbot(arena_data), self, 200, 100))
        self.bots.add(Realbot(navbot.Navbot(arena_data), self, 250, 100))
        self.bots.add(Realbot(stalkerbot.Stalkerbot(arena_data), self, 350, 250))
        self.bots.add(Realbot(stalkerbot.Stalkerbot(arena_data), self, 0, 0))
        self.bots.add(Realbot(playerbot.Playerbot(arena_data), self, 200, 350))

        # Declare another list that stores non-bots
        self.others = pygame.sprite.LayeredUpdates()

    """
    Remove any dead entities from the sprite group.
    """
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
        screen.blit(self.base_image, self.base_rect)
        self.walls.draw(screen)
        self.bots.draw(screen)
        self.others.draw(screen)
        #self.draw_sight(screen)

        # For now, just hardcode the entire arena to be redrawn
        return [self.base_rect]

    def draw_sight(self, screen):
        for bot in self.bots.sprites():
            r = bot.sight_range
            c = utils.geometry.get_center(bot.body)
            pygame.draw.circle(screen, pygame.Color("0x006600"), c, r, 1)
