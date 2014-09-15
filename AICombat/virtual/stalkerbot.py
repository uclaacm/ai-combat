"""
stalkerbot.py
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from virtual.navbot import Navbot

class Stalkerbot(Navbot):

    def __init__(self, arena_data):

        # Initialization
        Navbot.__init__(self, arena_data)
        self.image_path = "img/stalkerbot.png"

        # Stalkerbot stuff
        self.search_location = None
        self.destroy_target = None
        self.destroy_refresh = 0

    def delegate_action(self, status):
        pass

    def can_hit(self, enemy):
        return False

