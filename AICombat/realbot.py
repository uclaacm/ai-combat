"""
A "real bot" is the physical body of a bot, containing its sprite, position,
health, ammo, etc.
It is controlled by a "virtual bot," which is like the mind of the bot
"""

#Package imports
import pygame

#Local imports
from definitions import *
import resource

class Realbot(pygame.sprite.Sprite):

    def __init__(self, vbot):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.row, self.col = 0, 0
        self.state = state.WAITING
        self.direction = direction.RIGHT
        self.cooldown = 0
        self.vbot = vbot
        if vbot.imagePath:
            self.image, self.rect = resource.loadImage(vbot.imagePath)

    def update(self, arena, squares, elapsed):

        if self.cooldown - elapsed <= 0:
            # When it finishes cooling down
            if self.state == state.MOVING:
                self.row = self.nextRow
                self.col = self.nextCol
                self.rect.left = self.col*20
                self.rect.top = self.row*20

        self.cooldown = max(0, self.cooldown - elapsed)

        if self.cooldown > 0:
            if self.state == state.MOVING:
                self.rect.left = self.col*20 + 20*(-self.nextCol+self.col)*self.cooldown/500
                self.rect.top = self.row*20 + 20*(-self.nextRow+self.row)*self.cooldown/500

        else:
            self.state = state.WAITING
            act = self.vbot.getAction(squares, elapsed)
            if act == action.WAIT:
                return
            elif act == action.MOVE:
                nextRow = self.row + DR[self.direction]
                nextCol = self.col + DC[self.direction]
                if (nextRow < 0 or nextRow >= len(arena) or
                   nextCol < 0 or nextCol >= len(arena[0])):
                   return
                self.nextRow = nextRow
                self.nextCol = nextCol
                self.cooldown = 500
                self.state = state.MOVING
                return
