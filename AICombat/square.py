"""
square.py

Defines a square in the arena.
A square can theoretically hold multiple bots, multiple items, and has an
associated terrain type
"""


import definitions

class Square():

    def __init__(self, terrain = definitions.terrain.EMPTY):
        self.terrain = terrain
        self.items = []
        self.bots = []
        
