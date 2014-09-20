"""
playerbot.py

A virtualbot that is controlled by keyboard. Great for testing your skills
against the AI.
"""

# Global imports
import pygame

# Local imports
from virtual.queuebot import Queuebot

class Playerbot(Queuebot):

    def __init__(self, arena_data):

        # Initialization
        super(Playerbot, self).__init__(arena_data)
        self.image_path = "img/playerbot.png"

        # Playerbot stuff
        self.shoot_lock = False

    @Queuebot.queued
    def get_action(self, status):

        # Uses pygame to retrieve all keys currently being pressed
        keys = pygame.key.get_pressed()

        # Press space to shoot. Shooting has higher priority over moving
        # The shoot_lock prevents the bot from continuously shooting by forcing
        # the player to lift and press again
        if keys[pygame.K_SPACE]:
            if not self.shoot_lock:
                self.shoot_lock = True
                self.queue_shoot()
                return
        else:
            self.shoot_lock = False

        # Check the direction keys for movement. Pressing an arrow will
        # automatically queue the bot to turn to that direction, if not already
        # facing it, before moving.
        key_directions = [pygame.K_RIGHT, pygame.K_UP,
                          pygame.K_LEFT, pygame.K_DOWN]
        for i, k in enumerate(key_directions):
            if keys[k]:
                if self.direction != i:
                    diff = (i - self.direction) % 4
                    if diff == 1:
                        self.queue_left()
                    elif diff == 2:
                        self.queue_reverse()
                    elif diff == 3:
                        self.queue_right()
                self.queue_walk()
                return

        # If no action is being done, force the bot to stop
        self.queue_wait()
