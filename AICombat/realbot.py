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
        self.state = {"action": d.action.WAIT}

    """
    Called once per game loop iteration
    If the real bot is executing an action, it will continue executing it.
    Once it is done, it will ask the virtual bot for the next move.
    """
    def update(self, arena, elapsed):

        # Update state and return if not ready for next decision
        if not self._update_state(arena, elapsed):
            return

        # Compile status information to tell the virtualbot
        status = self._compile_status(arena, elapsed)

        # Ask virtualbot for what to do next
        decision = self.vbot.getAction(status)

        # Process decision
        self._process_decision(arena, decision)


    def _process_decision(self, arena, decision):

        # If walk
        if decision['action'] == d.action.WALK:
            # Check if parameters are valid
            if ("distance" not in decision or
                decision["distance"] <= 0):
                return
            self.state["action"] = d.action.WALK
            self.state["distance"] = decision["distance"]

        # If turn
        elif decision['action'] == d.action.TURN:
            # Check if parameters are valid
            if ("dir" not in decision or
                decision["dir"] != d.direction.LEFT and
                decision["dir"] != d.direction.RIGHT):
                return
            self.state["action"] = d.action.TURN
            self.state["next"] = (self.direction + 3 + decision["dir"]) % 4
            self.state["cooldown"] = d.duration.TURN

        # If shoot
        elif decision['action'] == d.action.SHOOT:
            # Center bullet on bot's position
            bullet_left = self.body.left + Realbot.SIZE[0]/2 - Bullet.SIZE[0]/2
            bullet_top = self.body.top + Realbot.SIZE[1]/2 - Bullet.SIZE[1]/2
            arena.others.add(Bullet(self, self.direction, bullet_left, bullet_top))
            self.state["action"] = d.action.SHOOT
            self.state["cooldown"] = d.duration.SHOOT


    def _update_state(self, arena, elapsed):

        action = self.state["action"]

        # If waiting
        if action == d.action.WAIT:
            return True

        # If turning
        if action == d.action.TURN:
            cooldown = self.state["cooldown"]
            cooldown = max(0, self.state["cooldown"] - elapsed)
            # Still turning
            if cooldown > 0:
                progress = 1 - float(cooldown) / d.duration.TURN
                deltaTheta = (self.state["next"] - self.direction)*90
                deltaTheta = deltaTheta if deltaTheta != 270 else -90
                theta = int(self.direction*90 + deltaTheta*progress)
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()
                self.state["cooldown"] = cooldown
                return False
            # Done turning
            else:
                self.direction = self.state["next"]
                theta = self.direction*90
                self.image = pygame.transform.rotate(self.baseImage, theta)
                self.center()
                self.state = {"action": d.action.WAIT}

        # If shooting
        elif action == d.action.SHOOT:
            cooldown = self.state["cooldown"]
            cooldown = max(0, self.state["cooldown"] - elapsed)
            # Still recoiling
            if cooldown > 0:
                self.state["cooldown"] = cooldown
                return False
            # Done recoiling
            else:
                self.state = {"action": d.action.WAIT}

        # If walking
        # TODO: Implement wall collision detection
        elif action == d.action.WALK:
            max_move = 20 / d.duration.WALK
            distance = self.state["distance"]
            amt = min(max_move, distance)
            nextTop = self.body.top + amt*d.DR[self.direction]
            nextLeft = self.body.left + amt*d.DC[self.direction]
            nextPosition = pygame.Rect(nextLeft, nextTop, 20, 20)
            # Can't walk out of arena
            if not arena.body.contains(nextPosition):
                self.state = {"action": d.action.WAIT}
                return True
            self.setPos(nextLeft, nextTop)
            distance -= amt
            # Still walking
            if distance:
                self.state["distance"] = distance
            else:
                self.state = {"action": d.action.WAIT}

        return True

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
