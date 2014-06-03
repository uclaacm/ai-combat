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

        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # Attach virtual bot
        self.vbot = vbot
        if vbot.imagePath:
            self.image, self.rect = resource.loadImage(vbot.imagePath)

        # Initialize action states
        self.action = action.WAIT
        self.cooldown = 0
        ### Location/move state
        self.row = 0
        self.col = 0
        self.nextRow = None
        self.nextCol = None
        ### Direction/turn state
        self.theta = 0
        self.direction = direction.RIGHT
        self.nextDirection = None


    def update(self, arena, squares, elapsed):

        # Update cooldown and check if it dropped below 0
        finished = self.cooldown - elapsed <= 0
        self.cooldown = max(0, self.cooldown - elapsed)

        # If hasn't finished yet (still executing an action)
        if not finished:
            # Smooth movement
            if self.action == action.MOVE:
                progress = 1 - float(self.cooldown) / duration.MOVE
                deltaCol = self.nextCol - self.col
                deltaRow = self.nextRow - self.row
                self.rect.left = int(20*(self.col + deltaCol*progress))
                self.rect.top = int(20*(self.row + deltaRow*progress))
            # Smooth turn
            elif self.action == action.LEFT or self.action == action.RIGHT:
                progress = 1 - float(self.cooldown) / duration.TURN
                deltaTheta = (self.nextDirection - self.direction)*90
                deltaTheta = deltaTheta if deltaTheta != 270 else -90
                self.theta = int(self.direction*90 + deltaTheta*progress)

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.action == action.MOVE:
                self.row = self.nextRow
                self.col = self.nextCol
                self.rect.left = self.col*20
                self.rect.top = self.row*20
            elif self.action == action.LEFT or self.action == action.RIGHT:
                self.direction = self.nextDirection
                self.theta = self.direction*90

        # If it finished cooling down, ask for the next action
        if finished:
            decision = self.vbot.getAction(squares, elapsed)
            if decision == action.MOVE:
                nextRow = self.row + DR[self.direction]
                nextCol = self.col + DC[self.direction]
                if (nextRow < 0 or nextRow >= len(arena) or
                   nextCol < 0 or nextCol >= len(arena[0])):
                   return
                self.nextRow = nextRow
                self.nextCol = nextCol
                self.cooldown = duration.MOVE
                self.action = decision
            elif decision == action.LEFT or decision == action.RIGHT:
                if decision == action.LEFT:
                    self.nextDirection = (self.direction + 3) % 4 #Modulus -1
                elif decision == action.RIGHT:
                    self.nextDirection = (self.direction + 5) % 4 #Modulus +1
                self.cooldown = duration.TURN
                self.action = decision
            else:
                self.action = action.WAIT
