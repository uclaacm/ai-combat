"""
enum.py

A hack to simulate C-style enums.
"""

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
