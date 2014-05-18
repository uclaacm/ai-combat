"""
Definitions for AICombat
"""

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

action = enum('MOVE', 'LEFT', 'RIGHT')
terrain = enum('EMPTY')
