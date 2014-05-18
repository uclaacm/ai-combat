"""
An extremely dumb virtual bot used for testing purposes
"""

from virtualbot import VirtualBot
from definitions import action

class Dumbbot(VirtualBot):

    def __init__(self):
        VirtualBot.__init__(self)

    def getAction(self, squares):
        return action.MOVE
