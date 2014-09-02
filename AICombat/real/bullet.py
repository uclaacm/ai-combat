"""
bullet.py

A basic bullet fired from a gun that all realbots have.
"""

# Global imports
import pygame

# Local imports
import real.definitions as d
from real.fighter import Fighter
from utils.geometry import predict_collision

class Bullet(Fighter):

    SIZE = (5, 5)

    def __init__(self, origin, walls, direction, left, top):

        # Call Entity init
        body = pygame.Rect(left, top, Bullet.SIZE[0], Bullet.SIZE[1])
        Fighter.__init__(self, "img/bullet.png", body, direction)
        self.center()

        # Other bookkeeping variables
        self.origin = origin
        self.speed = 6
        self.vel = (self.speed * d.DX[self.direction],
                    self.speed * d.DY[self.direction])
        self.max_dist = predict_collision(self.body, walls, *self.vel)

    """
    Called once per game loop iteration
    """
    def update(self, arena, elapsed):

        # Move
        self.move(*self.vel)
        self.max_dist -= self.speed
        if self.max_dist < 0:
            self.hp = 0
            return

        # Check for collision with any bots
        for bot in arena.bots.sprites():
            if bot is not self.origin and self.body.colliderect(bot.body):
                bot.hit(15)
                self.hp = 0
                return

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
