"""
bullet.py

A basic bullet shot from a gun that all realbots have
"""

# Global imports
import pygame

# Local imports
import definitions as d
from fighter import Fighter

class Bullet(Fighter):

    SIZE = (5, 5)

    def __init__(self, origin, direction, left, top):

        # Call Entity init
        body = pygame.Rect(left, top, Bullet.SIZE[0], Bullet.SIZE[1])
        Fighter.__init__(self, "bullet.png", body, direction)
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
