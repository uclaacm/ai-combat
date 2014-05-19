"""
A "virtual bot" is the mind of a physical "real bot"
It decides how the real bot in the arena should behave

This particular class is just a base class for specialized virtual bots to
build upon
"""

#global imports
import pygame

class Virtualbot():

    def __init__(self):
        pass

    def getAction(self, squares):
        pass
