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
import definitions as d

class Virtualbot():

    """
    The basic constructor for a virtualbot
        IN:  - dict containing initialization information about the arena and battle
    Only contains an empty imagePath. The virtual bot programmer can decide how
    the bot looks by providing the imagePath.
    """
    def __init__(self, arena_data):
        self.imagePath = None

    """
    Called whenever the realbot is ready to execute an action
        IN:  - a dict of various information about the bot state
        OUT: - a dict specifying the action to take and its parameters
    The default action is just to wait
    """
    def getAction(self, status):
        return {'action' : d.action.WAIT}
