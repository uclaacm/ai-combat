"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import Virtualbot
from definitions import action

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)
        self.counter = 0
        self.imagePath = "dumbbot.png"

    def getAction(self, squares, time):
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            return action.RIGHT
        return action.MOVE
