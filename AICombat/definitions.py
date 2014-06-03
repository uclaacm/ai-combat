"""
Definitions for AICombat
"""

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

action = enum('WAIT',
              'MOVE',
              'LEFT',
              'RIGHT')

terrain = enum('EMPTY')

direction = enum('RIGHT',
                 'DOWN',
                 'LEFT',
                 'UP')

duration = AttrDict({'WAIT': 0,
                     'MOVE': 300,
                     'TURN': 50
                    })

DR = [0, 1, 0, -1]
DC = [1, 0, -1, 0]
