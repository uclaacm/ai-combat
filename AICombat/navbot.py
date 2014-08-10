"""
navbot.py

A base virtualbot class that implements many useful navigation functions
"""

# Global imports
import pygame

# Local imports
import definitions as d
from virtualbot import Virtualbot

class Navbot(Virtualbot):

    class Waypoint():

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.neighbors = []
            self.unreachable = False

    def __init__(self, arena_data):
        Virtualbot.__init__(self, arena_data)
        self.imagePath = "navbot.png"

        # Declare navbot internals
        self.navbot_destination = None
        self.navbot_waypoints = []
        self.navbot_commands = []

        # Save arena layout
        self.arena_body = pygame.Rect(0, 0, arena_data["width"], arena_data["height"])
        self.arena_walls = arena_data["walls"]

        # Construct an extremely simple waypoint graph out of the arena. The
        # idea is to place a "waypoint" every 10 pixels. Ideally this will
        # split the the arena into 10x10 square chunks, and when computing a
        # path, the search algorithm will consider traversing only these
        # waypoints.
        ### Initialize waypoints
        for x in xrange(0, self.arena_body.width-Virtualbot.SIZE[0], 10):
            self.navbot_waypoints.append([])
            for y in xrange(0, self.arena_body.height-Virtualbot.SIZE[1], 10):
                self.navbot_waypoints[-1].append(Navbot.Waypoint(x, y))
        rows = len(self.navbot_waypoints)
        cols = len(self.navbot_waypoints[0])
        ### Detect unreachable waypoints (due to walls)
        for r in xrange(rows):
            for c in xrange(cols):
                wp = self.navbot_waypoints[r][c]
                wp_rect = pygame.Rect(wp.x, wp.y, Virtualbot.SIZE[0], Virtualbot.SIZE[1])
                for w in self.arena_walls:
                    if wp_rect.colliderect(w):
                        wp.unreachable = True
                        break
        ### Construct grid graph
        for r in xrange(rows):
            for c in xrange(cols):
                wp = self.navbot_waypoints[r][c]
                if wp.unreachable:
                    continue
                for i in xrange(4):
                    next_r = r+d.DR[i]
                    next_c = c+d.DC[i]
                    if (next_r < 0 or next_r >= rows or
                        next_c < 0 or next_c >= cols):
                       continue
                    next_wp = self.navbot_waypoints[next_r][next_c]
                    if next_wp.unreachable:
                        continue
                    wp.neighbors.append(next_wp)

    def setDestination(self, dest):
        if self.navbot_destination == dest:
            return
        x, y = dest

    def delegateAction(self, status):
        pass

    def getAction(self, status):

        is_ready = status["bot"]["status"] == d.action.WAIT

        res = self.delegateAction(status)
        if res:
            return res

        elif is_ready and len(self.navbot_commands) > 0:
            return self.navbot_commands.pop()

        else:
            return {"action": d.action.WAIT}
