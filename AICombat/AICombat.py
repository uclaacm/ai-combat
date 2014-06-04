#! /usr/bin/env python

"""
AI Combat
by AI@UCLA Gaming group
"""

import pygame
from battle import Battle

class Game():

    """
    Constructor for Game. Initializes pygame and sets up the window
    """
    def __init__(self):
        pygame.init()

        width = 800
        height = 600
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI Combat")
        self.clock = pygame.time.Clock()
        self.battle = Battle()

    """
    Starts the game by entering into the infinite game loop
    """
    def start(self):
        while 1:
            # Sleep in such a way that the game does not exceed 30 FPS
            elapsed = self.clock.tick(40)

            # Event processing
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                events.append(event)

            # Update battle state
            self.battle.update(events, elapsed)
            
            # Paint stuff (does not actually paint until you call
            # pygame.display.flip)
            self.screen.fill((0,0,0))
            self.battle.draw(self.screen)
            
            # Paint the screen
            pygame.display.flip()


"""
When AICombat.py is run, it will more or less skip everything until it sees the
if statement at the end. The statement calls main(), which creates a Game
object to handle the actual application/pygame logic

Order of execution:
if statement --> main() --> Game.__init__() --> Game.start()
"""

def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
