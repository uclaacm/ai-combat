"""
A "real bot" is the physical body of a bot, containing its sprite, position,
health, ammo, etc.
It is controlled by a "virtual bot," which is like the mind of the bot
"""

#Package imports
import pygame

#Local imports
from definitions import action
import resource

class Realbot(pygame.sprite.Sprite):

    def __init__(self, vbot):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.loc = (0, 0)
        self.direction = 0
        self.image = None
        self.rect = None
        self.cooldown = 0
        self.vbot = vbot

    def isReady(self):
        return self.cooldown <= 0
