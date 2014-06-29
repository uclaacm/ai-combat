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

    def __init__(self, vbot, top=0, left=0):

        # Call Sprite initializer
        pygame.sprite.Sprite.__init__(self)

        # Attach virtual bot
        self.vbot = vbot
        if vbot.imagePath:
            self.baseImage, self.baseRect = resource.loadImage(vbot.imagePath)
            self.image = self.baseImage
            self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left

        # Initialize action states
        self.action = action.WAIT
        self.cooldown = 0
        ### Direction/turn state
        self.theta = 0
        self.direction = direction.RIGHT
        self.nextDirection = None
        self.pivotLeft = None
        self.pivotTop = None

    """
    Called once per game loop iteration
    If the real bot is executing an action, it will continue executing it.
    Once it is done, it will ask the virtual bot for the next move.
    """
    def update(self, arena, elapsed):

        # Update cooldown and check if it dropped below 0
        finished = self.cooldown - elapsed <= 0
        self.cooldown = max(0, self.cooldown - elapsed)

        # If hasn't finished yet (still executing an action)
        if not finished:
            # Smooth turn
            if self.action == action.TURN:
                progress = 1 - float(self.cooldown) / duration.TURN
                deltaTheta = (self.nextDirection - self.direction)*90
                deltaTheta = deltaTheta if deltaTheta != 270 else -90
                self.theta = int(self.direction*90 + deltaTheta*progress)
                self.image = pygame.transform.rotate(self.baseImage, self.theta)
                r = self.image.get_rect()
                self.rect.left = self.pivotLeft - (r.width-20)/2
                self.rect.top = self.pivotTop - (r.height-20)/2

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.action == action.TURN:
                self.direction = self.nextDirection
                self.theta = self.direction*90
                self.image = pygame.transform.rotate(self.baseImage, self.theta)
                self.rect.left = self.pivotLeft
                self.rect.top = self.pivotTop

        # If it finished cooling down, ask for the next action
        if finished:

            # Assume wait until proven otherwise
            self.action = action.WAIT

            # Compute what objects are in the bot's sight
            objects = []

            # Ask virtualbot for what to do next
            decision = self.vbot.getAction(objects, elapsed)

            # If the decision is to move
            if decision['action'] == action.MOVE:
                
                nextTop = self.rect.top + 4*DR[self.direction]
                nextLeft = self.rect.left + 4*DC[self.direction]
                if (nextTop < 0 or nextTop+20 >= arena.height or
                   nextLeft < 0 or nextLeft+20 >= arena.width):
                   return
                self.rect.top = nextTop
                self.rect.left = nextLeft

            # If the decision is to turn (in a valid direction)
            elif (decision['action'] == action.TURN and
                  'dir' in decision and
                  decision['dir'] != direction.UP and
                  decision['dir'] != direction.DOWN):
                self.pivotLeft = self.rect.left
                self.pivotTop = self.rect.top
                self.nextDirection = (self.direction + 3 + decision['dir']) % 4
                self.cooldown = duration.TURN
                self.action = decision['action']
