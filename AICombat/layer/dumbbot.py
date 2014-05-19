"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import Virtualbot
from definitions import action

class Dumbbot(Virtualbot):

    def __init__(self):
        Virtualbot.__init__(self)

    def getAction(self, squares):
        return action.MOVE
