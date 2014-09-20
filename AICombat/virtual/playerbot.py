"""
playerbot.py

A virtualbot that is controlled by keyboard. Great for testing your skills
against the AI.
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
        self.key_directions = [pygame.K_RIGHT, pygame.K_UP,
                               pygame.K_LEFT, pygame.K_DOWN]
        self.shoot_lock = False


    def get_action(self, status):

        self.update_status(status)

        # Alias the actions for easy use
        # This is very ugly; will try to fix later
        LEFT_TURN = {"action": d.action.TURN,
                     "direction": d.direction.LEFT}
        RIGHT_TURN = {"action": d.action.TURN,
                      "direction": d.direction.RIGHT}
        SHOOT = {"action": d.action.SHOOT}
        WALK = {"action": d.action.WALK,
                "distance": 20}
        WAIT = {"action": d.action.WAIT}

        # Uses pygame to retrieve all keys currently being pressed
        keys = pygame.key.get_pressed()

        # Press space to shoot. Shooting has higher priority over moving
        # The shoot_lock prevents the bot from continuously shooting by forcing
        # the player to lift and press again
        if keys[pygame.K_SPACE]:
            if not self.shoot_lock:
                self.shoot_lock = True
                return SHOOT
        else:
            self.shoot_lock = False

        # Check the direction keys for movement. Pressing an arrow will
        # automatically compel the bot to turn to that direction, if not already
        # facing it, before moving.
        for i, k in enumerate(self.key_directions):
            if keys[k]:
                if self.direction != i:
                    diff = i - self.direction
                    if diff % 4 <= 2:
                        return LEFT_TURN
                    else:
                        return RIGHT_TURN
                return WALK

        return WAIT
