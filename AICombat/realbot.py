"""
realbot.py

A "real bot" is the physical body of a bot, containing its sprite, position,
health, ammo, etc. It is controlled by a "virtual bot," which is like the mind
of the bot. When the real bot is in a WAIT state, it will ask its virtual bot
what action to take next. Given an action, the real bot will take appropriate
steps to execute it properly.
"""

# Global imports
import pygame

# Local imports
from definitions import *
import resource

class Realbot(pygame.sprite.Sprite):

    def __init__(self, vbot):

        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # Attach virtual bot
        self.vbot = vbot
        if vbot.imagePath:
            self.baseImage, self.baseRect = resource.loadImage(vbot.imagePath)
            self.image = self.baseImage
            self.rect = self.image.get_rect()

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

    """
    Called once per game loop iteration
    If the real bot is executing an action, it will continue executing it.
    Once it is done, it will ask the virtual bot for the next move.
    """
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
            elif self.action == action.TURN:
                progress = 1 - float(self.cooldown) / duration.TURN
                deltaTheta = (self.nextDirection - self.direction)*90
                deltaTheta = deltaTheta if deltaTheta != 270 else -90
                self.theta = int(self.direction*90 + deltaTheta*progress)
                self.image = pygame.transform.rotate(self.baseImage, self.theta)
                r = self.image.get_rect()
                self.rect.left = self.col*20 - (r.width-20)/2
                self.rect.top = self.row*20 - (r.height-20)/2

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.action == action.MOVE:
                self.row = self.nextRow
                self.col = self.nextCol
                self.rect.left = self.col*20
                self.rect.top = self.row*20
            elif self.action == action.TURN:
                self.direction = self.nextDirection
                self.theta = self.direction*90
                self.image = pygame.transform.rotate(self.baseImage, self.theta)
                self.rect.left = self.col*20
                self.rect.top = self.row*20

        # If it finished cooling down, ask for the next action
        if finished:

            # Assume wait until proven otherwise
            self.action = action.WAIT

            # Ask virtualbot for what to do next
            decision = self.vbot.getAction(squares, elapsed)

            # If the decision is to move
            if decision['action'] == action.MOVE:
                nextRow = self.row + DR[self.direction]
                nextCol = self.col + DC[self.direction]
                if (nextRow < 0 or nextRow >= len(arena) or
                   nextCol < 0 or nextCol >= len(arena[0])):
                   return
                self.nextRow = nextRow
                self.nextCol = nextCol
                self.cooldown = duration.MOVE
                self.action = decision['action']

            # If the decision is to turn (in a valid direction)
            elif (decision['action'] == action.TURN and
                  'dir' in decision and
                  decision['dir'] != direction.UP and
                  decision['dir'] != direction.DOWN):
                self.nextDirection = (self.direction + 3 + decision['dir']) % 4
                self.cooldown = duration.TURN
                self.action = decision['action']
