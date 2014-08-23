#! /usr/bin/env python

"""
AI Combat
by AI@UCLA Gaming group

AICombat is a top-down shooter in which programmable AI bots battle each other
in a closed arena.  https://github.com/EaterOA/AICombat

AICombat.py is the application class, which handles the pygame window, game
clock, and main game loop.
"""

# Global imports
import pygame

# Local imports
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
        # For now, start directly in Battle mode
        # Other modes in the future may include menu, settings, splash, etc.
        self.battle = Battle()
        self.game_tick = 20

    """
    Starts the game by entering into the infinite game loop
    """
    def start(self):

        elapsed = 0
        while 1:
            # Sleep in such a way that the game does not exceed 60 FPS
            # (This value is completely arbitrary)
            elapsed += self.clock.tick(60)

            while elapsed >= self.game_tick:
                # Event processing
                events = []
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    events.append(event)

                # Update battle state
                self.battle.update(events, self.game_tick)
                elapsed -= self.game_tick

            # Paint stuff (does not actually paint until you call
            # pygame.display.update)
            # The list of rects returned by the draw tells pygame.display
            # which parts to actually draw
            rects = self.battle.draw(self.screen)

            # Paint the screen
            pygame.display.update(rects)

"""
When AICombat.py is run, it will more or less skip everything until it sees the
if statement at the end. The statement calls main(), which creates a Game
object to handle the actual application/pygame logic

Order of execution: if statement --> main() --> Game.__init__() --> Game.start()
"""
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
