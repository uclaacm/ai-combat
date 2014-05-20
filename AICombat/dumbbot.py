"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import Virtualbot
from definitions import action

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)
        self.imagePath = "dumbbot.png"

    def getAction(self, squares, time):
        return action.MOVE
