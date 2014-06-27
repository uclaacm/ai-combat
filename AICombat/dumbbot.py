"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import Virtualbot
from definitions import *

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)
        self.counter = 0
        self.imagePath = "dumbbot.png"

    def getAction(self, objects, time):
        decision = {}

        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            decision['action'] = action.TURN
            decision['dir'] = direction.RIGHT
        else:
            decision['action'] = action.MOVE

        return decision
