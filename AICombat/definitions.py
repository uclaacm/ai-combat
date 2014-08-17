"""
definitions.py

Various definitions for AICombat.
The technical details of how the objects are being defined don't really matter (although it may be interesting). Mainly, this file is important for declaring constants such as allowable bot actions, etc.
"""

# Some hack to recreate C-style enums
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Some hack to recreate clean, attribute-indexable dictionaries
# e.g. object.value as opposed to object["value"]
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# Legal bot actions
action = enum('WAIT',
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
                     'WALK': 5,   # 5 ms per pixel
                     'TURN': 100, # 100 ms per 90 degrees
                     'SHOOT': 100 # 100 ms per shot
                    })

# Convenience (row, col) mappings for each cardinal direction
DR = [0, -1, 0, 1]
DC = [1, 0, -1, 0]
