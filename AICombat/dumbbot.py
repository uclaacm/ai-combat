"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import Virtualbot
from definitions import *

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)
        self.counter = 0
        self.outer = 1
        self.imagePath = "dumbbot.png"

    def getAction(self, objects, time):
        decision = {}

        self.counter += 1
        if self.counter == self.outer*5:
            self.outer += 1
            self.counter = 0
            decision['action'] = action.TURN
            decision['dir'] = direction.RIGHT
        elif self.counter == self.outer*5-1:
            decision['action'] = action.SHOOT
        else:
            decision['action'] = action.MOVE

        return decision
