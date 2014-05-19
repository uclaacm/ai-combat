# global imports
import pygame

# local imports
import resource
from definitions import terrain, action
from square import Square
from realbot import Realbot
from dumbbot import Dumbbot

class Battle():

    def __init__(self):

        # Load terrain tiles
        self.terrainImages = {}
        self.terrainImages[terrain.EMPTY] = resource.loadImage("terrain_empty.png")

        # Initialize arena squares and image
        rows = 20
        cols = 20
        self.arena = []
        for row in xrange(rows):
            self.arena.append([])
            for col in xrange(cols):
                 self.arena[-1].append(Square())
        self.arenaRect = pygame.Rect(0, 0, rows*20, cols*20)
        self.arenaImage = pygame.Surface(self.arenaRect.size).convert()
        self.arenaImage.fill((255,255,255))
        for row in xrange(rows):
            for col in xrange(cols):
                self.arenaImage.blit(self.terrainImages[self.arena[row][col].terrain][0], (row*20,col*20))

        # Initialize real bots
        # For now, hardcode in a Dumbbot
        self.bots = [Realbot(Dumbbot())]

        # Initialize other bookkeeping variables
        self.totalElapsed = 0


    def update(self, events, elapsed):
        self.totalElapsed += elapsed

    def draw(self, screen):
        screen.blit(self.arenaImage, self.arenaRect)
