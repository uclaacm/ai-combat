"""
virtualbot.py

A "virtual bot" is the mind of a physical "real bot." It decides how the real
bot in the arena should behave.  When a real bot is in a WAIT state, it will
ask a virtual bot for an action to perform. The virtual bot will be given
information on the real bot's current state and vision, and decide on an action
accordingly.

This particular class is just a base class for specialized virtual bots to
build upon.
"""

# Global imports
import pygame

# Local imports
from definitions import action

class Virtualbot():

    def __init__(self):
        # All virtual bots have an imagePath
        # The virtual bot programmer decides how the bot should look
        self.imagePath = None

    def getAction(self, squares, time):
        return action.WAIT
