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

        # Update cooldown and check if it dropped below 0
        finished = self.cooldown - elapsed <= 0
        self.cooldown = max(0, self.cooldown - elapsed)

        # If hasn't finished yet (still executing an action)
        if not finished:
            # Execute smooth movement
            if self.state == state.MOVING:
                progress = 1 - float(self.cooldown) / duration['MOVE']
                deltaCol = self.nextCol - self.col
                deltaRow = self.nextRow - self.row
                self.rect.left = int(20*(self.col + deltaCol*progress))
                self.rect.top = int(20*(self.row + deltaRow*progress))

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.state == state.MOVING:
                self.row = self.nextRow
                self.col = self.nextCol
                self.rect.left = self.col*20
                self.rect.top = self.row*20

        # If it finished cooling down, ask for the next action
        if finished:
            act = self.vbot.getAction(squares, elapsed)
            if act == action.MOVE:
                nextRow = self.row + DR[self.direction]
                nextCol = self.col + DC[self.direction]
                if (nextRow < 0 or nextRow >= len(arena) or
                   nextCol < 0 or nextCol >= len(arena[0])):
                   return
                self.nextRow = nextRow
                self.nextCol = nextCol
                self.cooldown = duration['MOVE']
                self.state = state.MOVING
            else:
                self.state = state.WAITING
