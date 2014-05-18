"""
A "real bot" is the physical body of a bot, containing its sprite, position,
health, ammo, etc.
It is controlled by a "virtual bot," which is like the mind of the bot
"""

#Package imports
import pygame

#Local imports
import actions
import resource

class RealBot(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.direction = 0
        self.image = None
        self.rect = None
        self.cooldown = 0

    def isReady(self):
        return self.cooldown <= 0
