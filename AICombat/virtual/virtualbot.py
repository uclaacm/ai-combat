"""
virtualbot.py

A "virtualbot" is the mind of a physical "realbot." It decides how the realbot
in the arena should behave.  When a realbot is in a WAIT state, it will
ask a virtualbot for an action to perform. The virtualbot will be given
information on the realbot's current state and what it sees, and decide on an
action accordingly.

This particular class is just a base class for specialized virtualbots to
build upon. It contains some utility functions that most virtualbots may find
useful.
"""

# Local imports
import real.definitions as d

class Virtualbot(object):

    SIZE = (20, 20)

    """
    The basic constructor for a virtualbot
    IN:  - dict containing initialization information about the arena
    The virtual bot programmer can decide how the bot looks by providing the
    image_path.
    """
    def __init__(self, arena_data):
        self.image_path = None
        self.state = None
        self.body = None
        self.hp = None
        self.ammo = None
        self.direction = None

    """
    Called whenever the realbot is ready to execute an action
    IN:  - a dict of various information about the bot status
    OUT: - a dict specifying the action to take and its parameters
    The default action is just to continue (doing nothing)
    """
    def get_action(self, status):
        return {'action' : d.action.CONTINUE}

    """
    Utility function to automatically store vital status attributes
    IN:  - realbot status dict
    """
    def update_status(self, status):
        self.state = status["state"]
        self.body = status["body"]
        self.hp = status["hp"]
        self.ammo = status["ammo"]
        self.direction = status["direction"]
