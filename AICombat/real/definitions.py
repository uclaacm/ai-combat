"""
definitions.py

Various definitions and utility functions for real entities in AICombat.
Mainly, this file is important for declaring constants such as allowable bot
actions, etc.
"""

# Global imports
import random

# Local imports
from utils.enum import enum
from utils.attrdict import AttrDict

_id_database = set()

def generate_id():
    new_id = random.getrandbits(64)
    while new_id in _id_database:
        new_id = random.getrandbits(64)
    return new_id

# Legal bot actions
action = enum('WAIT',
              'CONTINUE',
              'WALK',
              'TURN',
              'SHOOT')

# Legal cardinal directions
direction = enum('RIGHT',
                 'UP',
                 'LEFT',
                 'DOWN')

# Constants describing how long each bot action takes
duration = AttrDict({'WAIT': 0,
                     'CONTINUE': 0,
                     'WALK': 5,     # 5 ms per pixel
                     'TURN': 100,   # 100 ms per 90 degrees
                     'SHOOT': 100   # 100 ms per shot
                    })

# Convenience (x, y) mappings for each cardinal direction
DX = [1, 0, -1, 0]
DY = [0, -1, 0, 1]
