"""
playerbot.py
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from virtual.virtualbot import Virtualbot

class Playerbot(Virtualbot):

    def __init__(self, arena_data):

        # Initialization
        Virtualbot.__init__(self, arena_data)
        self.image_path = "img/playerbot.png"

        # Playerbot stuff
        self.shoot_lock = False


    def get_action(self, status):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if not self.shoot_lock:
                self.shoot_lock = True
                return {"action": d.action.SHOOT}
        else:
            self.shoot_lock = False

