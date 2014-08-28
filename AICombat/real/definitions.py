"""
definitions.py

Various definitions for AICombat.
The technical details of how the objects are being defined don't really matter (although it may be interesting). Mainly, this file is important for declaring constants such as allowable bot actions, etc.
"""

from utils.enum import enum
from utils.attrdict import AttrDict

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

# Convenience (row, col) mappings for each cardinal direction
DR = [0, -1, 0, 1]
DC = [1, 0, -1, 0]
