"""
An extremely dumb virtual bot used for testing purposes
"""

# Global imports
import random

# Local imports
import definitions as d
from virtualbot import Virtualbot

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)
        self.imagePath = "dumbbot.png"

    def getAction(self, objects, time):
        decision = {}

        roll = random.randint(0,99)
        if roll < 80:
            decision['action'] = d.action.MOVE
        elif roll < 95:
            decision['action'] = d.action.TURN
            decision['dir'] = d.direction.RIGHT
        else:
            decision['action'] = d.action.SHOOT

        return decision
