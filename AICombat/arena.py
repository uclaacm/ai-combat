"""
arena.py
"""

# Global imports
import pygame

# Local imports
import resource
from definitions import action
from realbot import Realbot
from dumbbot import Dumbbot

class Arena(pygame.sprite.Sprite):

    def __init__(self):

        # Load arena image
        self.baseImage, self.baseRect = resource.loadImage("arena.png")

        # Initialize real bots
        # For now, hardcode in a Dumbbot for testing
        self.bots = pygame.sprite.LayeredUpdates()
        self.bots.add(Realbot(Dumbbot()))

        # Declare another list that stores non-bots
        self.others = pygame.sprite.LayeredUpdates()

        # Initialize bookkeeping variables
        self.height = 400
        self.width = 400

    """
    Called once per game loop iteration
    Updates all bot actions
    """
    def update(self, events, elapsed):
        self.bots.get_sprite(0).update(self, elapsed)

    """
    Called once per game loop iteration
    Clears the arena and redraws the bots in updated positions
    """
    def draw(self, screen):
        screen.blit(self.baseImage, self.baseRect)
        self.bots.draw(screen)
