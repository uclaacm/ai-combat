"""
Definitions for AICombat
"""

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

action = enum('WAIT',
              'MOVE',
              'LEFT',
              'RIGHT')

terrain = enum('EMPTY')

direction = enum('UP',
                 'DOWN',
                 'LEFT',
                 'RIGHT')

state = enum('WAITING',
             'MOVING',
             'TURNING'
            )

duration = {'WAIT': 0,
            'MOVE': 300,
            'LEFT': 50,
            'RIGHT': 50
           }

DR = [-1, 1, 0, 0]
DC = [0, 0, -1, 1]
