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
import definitions as d
from fighter import Fighter
from bullet import Bullet
from util import *

class Realbot(Fighter):

    SIZE = (20, 20)

    def __init__(self, vbot, left=0, top=0):

        # Attach virtual bot
        self.vbot = vbot

        # Call Fighter init
        body = pygame.Rect(left, top, Realbot.SIZE[0], Realbot.SIZE[1])
        Fighter.__init__(self, vbot.imagePath, body, hp=100)

        # Initialize states
        self.ammo = 10
        self.state = d.action.WAIT
        self.cooldown = 0
        self.nextDirection = None

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
            if self.state == d.action.TURN:
                progress = 1 - float(self.cooldown) / d.duration.TURN
                deltaTheta = (self.nextDirection - self.direction)*90
                deltaTheta = deltaTheta if deltaTheta != 270 else -90
                theta = int(self.direction*90 + deltaTheta*progress)
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()

        # If it finished cooling down, make any final adjustments
        if finished:
            if self.state == d.action.TURN:
                self.direction = self.nextDirection
                theta = self.direction*90
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()

        # If it finished cooling down, ask for the next action
        if finished:

            # Assume wait until proven otherwise
            self.state = d.action.WAIT

            # Compile status information to tell the virtualbot
            status = self._compile_status(arena, elapsed)

            # Ask virtualbot for what to do next
            decision = self.vbot.getAction(status)

            # If the decision is to move
            if decision['action'] == d.action.MOVE:

                nextTop = self.body.top + 4*d.DR[self.direction]
                nextLeft = self.body.left + 4*d.DC[self.direction]
                nextPosition = pygame.Rect(nextLeft, nextTop, 20, 20)
                if arena.body.contains(nextPosition):
                    self.setPos(nextLeft, nextTop)

            # If the decision is to turn (in a valid direction)
            elif (decision['action'] == d.action.TURN and
                  'dir' in decision and
                  decision['dir'] != d.direction.UP and
                  decision['dir'] != d.direction.DOWN):
                self.nextDirection = (self.direction + 3 + decision['dir']) % 4
                self.cooldown = d.duration.TURN
                self.state = decision['action']

            elif decision['action'] == d.action.SHOOT:

                # Center bullet on bot's position
                bullet_left = self.body.left + Realbot.SIZE[0]/2 - Bullet.SIZE[0]/2
                bullet_top = self.body.top + Realbot.SIZE[1]/2 - Bullet.SIZE[1]/2
                arena.others.add(Bullet(self, self.direction, bullet_left, bullet_top))
                self.cooldown = d.duration.SHOOT
                self.state = decision['action']

    def get_info(self):

        info = {}

        # Type
        info["entity"] = "bot"

        # Bot information
        info["bot"] = {}
        info["bot"]["state"] = self.state
        info["bot"]["hp"] = self.hp
        info["bot"]["ammo"] = self.ammo
        info["bot"]["direction"] = self.direction
        info["bot"]["body"] = self.body

        return info

    def _compile_status(self, arena, elapsed):

        # Bot information
        status = self.get_info()

        # Environment information
        status["elapsed"] = elapsed

        # Objects of interest in sight range
        status["objects"] = {}
        status["objects"]["bots"] = []
        center = get_center(self.body)
        # Temporary method: circle with radius 100
        sight = pygame.Rect(center[0], center[1], 100, 100)
        for entity in arena.bots.sprites():
            if entity != self and collide_rect_circle(entity.body, sight):
                status["objects"]["bots"].append(entity.get_info())
        status["objects"]["projectiles"] = []
        status["objects"]["items"] = []

        return status
