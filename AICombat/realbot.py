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
from entity import Entity

class Realbot(Entity):

    def __init__(self, vbot, left=0, top=0):

        # Attach virtual bot
        self.vbot = vbot

        # Call Entity init
        body = pygame.Rect(left, top, 20, 20)
        Entity.__init__(self, vbot.imagePath, body)

        # Initialize status
        self.hp = 100
        self.ammo = 10
        # Initialize action states
        self.action = action.WAIT
        self.cooldown = 0
        ### Direction/turn state
        self.nextDirection = None

    """
    Called when the realbot is struck by a bullet
    """
    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            pass

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
                theta = int(self.direction*90 + deltaTheta*progress)
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.action == action.TURN:
                self.direction = self.nextDirection
                theta = self.direction*90
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()

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
                
                nextTop = self.body.top + 4*DR[self.direction]
                nextLeft = self.body.left + 4*DC[self.direction]
                nextPosition = pygame.Rect(nextLeft, nextTop, 20, 20)
                if arena.body.contains(nextPosition):
                    self.setPos(nextLeft, nextTop)

            # If the decision is to turn (in a valid direction)
            elif (decision['action'] == action.TURN and
                  'dir' in decision and
                  decision['dir'] != direction.UP and
                  decision['dir'] != direction.DOWN):
                self.nextDirection = (self.direction + 3 + decision['dir']) % 4
                self.cooldown = duration.TURN
                self.action = decision['action']
