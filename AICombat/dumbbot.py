"""
An extremely dumb virtual bot used for testing purposes
"""

# Global imports
import random

# Local imports
import definitions as d
from virtualbot import Virtualbot

class Dumbbot(Virtualbot):

    def __init__(self, arena_data):
        Virtualbot.__init__(self, arena_data)
        self.imagePath = "dumbbot.png"

    def getAction(self, status):

        decision = {}

        roll = random.randint(0, 99)
        if roll < 30:
            decision['action'] = d.action.CONTINUE
        elif roll < 80:
            decision['action'] = d.action.WALK
            decision['distance'] = random.randint(1,10)
        elif roll < 95:
            decision['action'] = d.action.TURN
            decision['direction'] = d.direction.RIGHT
        else:
            decision['action'] = d.action.SHOOT

        return decision
