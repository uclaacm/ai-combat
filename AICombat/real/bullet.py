"""
bullet.py

A basic bullet fired from a gun that all realbots have.
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from real.fighter import Fighter

class Bullet(Fighter):

    SIZE = (5, 5)

    def __init__(self, origin, direction, left, top):

        # Call Entity init
        body = pygame.Rect(left, top, Bullet.SIZE[0], Bullet.SIZE[1])
        Fighter.__init__(self, "img/bullet.png", body, direction)
        self.center()

        # Other bookkeeping variables
        self.vel = 4
        self.origin = origin

    """
    Called once per game loop iteration
    """
    def update(self, arena, elapsed):

        # Move
        self.move(self.vel*d.DC[self.direction], self.vel*d.DR[self.direction])

        # Check for collision with any bots
        for bot in arena.bots.sprites():
            if bot is not self.origin and self.body.colliderect(bot.body):
                bot.hit(15)
                self.hp = 0
                return

        # Check if out of screen
        if not arena.body.colliderect(self.body):
            self.hp = 0

    """
    Override of Entity's get_info()
    """
    def get_info(self):

        info = {}

        # Type
        info["entity"] = "bullet"

        # Bullet information
        info["bullet"] = {}
        info["bullet"]["direction"] = self.direction
        info["bullet"]["body"] = self.body

        return info
