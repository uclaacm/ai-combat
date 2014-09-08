"""
realbot.py

A "realbot" is the physical body of a bot, containing its sprite, position,
health, ammo, etc. It is controlled by a "virtualbot," which is like the mind
of the bot. When the realbot is in a WAIT state, it will ask its virtualbot
what action to take next. Given an action, the realbot will take appropriate
steps to execute it properly.
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from real.fighter import Fighter
from real.bullet import Bullet
from utils.geometry import *

class Realbot(Fighter):

    SIZE = (20, 20)

    def __init__(self, vbot, arena, left=0, top=0):

        # Attach virtualbot
        self.vbot = vbot

        # Call Fighter init
        body = pygame.Rect(left, top, Realbot.SIZE[0], Realbot.SIZE[1])
        Fighter.__init__(self, vbot.image_path, body, hp=100)

        # Initialize states
        self.ammo = 10
        self.state = {"action": d.action.WAIT}
        width = arena.body.width
        height = arena.body.height
        self.arena_walls = [w.body for w in arena.walls.sprites()]
        # Treat the arena boundaries as walls
        self.arena_walls.append(pygame.Rect(-1, -1, width+1, 1))
        self.arena_walls.append(pygame.Rect(-1, 0, 1, height+1))
        self.arena_walls.append(pygame.Rect(0, height, width+1, 1))
        self.arena_walls.append(pygame.Rect(width, -1, 1, height+1))

    """
    Called once per game loop iteration
    If the realbot is executing an action, it will continue executing it.
    Once it is done, it will ask the virtualbot for the next move.
    """
    def update(self, arena, elapsed):

        # Update state and return if not ready for next decision
        if not self._update_state(arena, elapsed):
            return

        # Compile status information to tell the virtualbot
        status = self._compile_status(arena, elapsed)

        # Ask virtualbot for what to do next
        decision = self.vbot.get_action(status)

        # Process decision
        self._process_decision(arena, decision)


    """
    Given the virtualbot's decision, adjust the state accordingly
    """
    def _process_decision(self, arena, decision):

        # If continue, simply do nothing
        if decision['action'] == d.action.CONTINUE:
            return

        # If wait, toggle action state
        elif decision['action'] == d.action.WAIT:
            self.state["action"] = d.action.WAIT

        # If walk, toggle action state and retrieve distance
        elif decision['action'] == d.action.WALK:
            # Check if parameters are valid
            if ("distance" not in decision or
                decision["distance"] <= 0):
                return
            max_distance = predict_collision(self.body, self.arena_walls,
                                             d.DX[self.direction],
                                             d.DY[self.direction])
            self.state["max_distance"] = max_distance
            self.state["action"] = d.action.WALK
            self.state["distance"] = decision["distance"]

        # If turn, toggle action state and compute next direction
        elif decision['action'] == d.action.TURN:
            # Check if parameters are valid
            if ("direction" not in decision or
                decision["direction"] != d.direction.LEFT and
                decision["direction"] != d.direction.RIGHT):
                return
            self.state["action"] = d.action.TURN
            self.state["next"] = (self.direction + 3 + decision["direction"]) % 4
            self.state["cooldown"] = d.duration.TURN

        # If shoot, toggle action state and materialize the bullet
        elif decision['action'] == d.action.SHOOT:
            # Center bullet on bot's position
            bullet_left = self.body.left + Realbot.SIZE[0]/2 - Bullet.SIZE[0]/2
            bullet_top = self.body.top + Realbot.SIZE[1]/2 - Bullet.SIZE[1]/2
            arena.others.add(Bullet(self, self.arena_walls, self.direction, bullet_left, bullet_top))
            self.state["action"] = d.action.SHOOT
            self.state["cooldown"] = d.duration.SHOOT

    """
    Forwards the realbot's state, e.g. move forward if walking.
    """
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
                dTheta = (self.state["next"] - self.direction)*90
                dTheta = dTheta if abs(dTheta) != 270 else -dTheta/3
                theta = int(self.direction*90 + dTheta*progress)
                self.image = pygame.transform.rotate(self.base_image, theta)
                self.center()
                self.state["cooldown"] = cooldown
                return False
            # Done turning
            else:
                self.direction = self.state["next"]
                theta = self.direction*90
                self.image = pygame.transform.rotate(self.base_image, theta)
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
        elif action == d.action.WALK:
            max_move = 20 / d.duration.WALK
            distance = self.state["distance"]
            # max_distance is a previously calculated value that indicates when
            # the bot will collide with a wall
            max_distance = self.state["max_distance"]
            amt = min(max_move, distance, max_distance)
            next_top = self.body.top + amt*d.DY[self.direction]
            next_left = self.body.left + amt*d.DX[self.direction]
            self.set_pos(next_left, next_top)
            distance -= amt
            max_distance -= amt
            # Still walking
            if distance and max_distance:
                self.state["distance"] = distance
                self.state["max_distance"] = max_distance
            else:
                self.state = {"action": d.action.WAIT}

        return True

    """
    Override of Entity's get_info() to provide public information about the bot
    """
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

    """
    Compiles the status of the realbot to give to the virtualbot
    """
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
