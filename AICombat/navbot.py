"""
navbot.py

A base virtualbot class that implements many useful navigation functions
"""

# Global imports
import pygame
import math
from Queue import Queue

# Local imports
import definitions as d
from virtualbot import Virtualbot

class Navbot(Virtualbot):

    class Waypoint():

        def __init__(self, x, y, h, d):
            self.x = x
            self.y = y
            self.heuristic = h
            self.distance = d
            self.priority = h + d
            self.neighbors = []

    def __init__(self, arena_data):

        Virtualbot.__init__(self, arena_data)
        self.imagePath = "navbot.png"

        # Declare navbot internals
        self.navbot_destination = None
        self.navbot_waypoints = []
        self.navbot_commands = []
        self.navbot_reachable = []

        # Save arena layout
        self.arena_body = pygame.Rect(0, 0, arena_data["width"], arena_data["height"])
        self.arena_walls = arena_data["walls"]

        # Compute all reachable and unreachable pixels
        # Won't use _too_ much memory as long as the map isn't too big....
        # Allows O(1) path collision detection instead of O(len(walls))
        # Also allows easier construction of waypoint grid during path finding
        for x in xrange(self.arena_body.width):
            self.navbot_reachable.append([True] * self.arena_body.height)
        for w in self.arena_walls:
            leftbound = max(0, w.left - Virtualbot.SIZE[0])
            rightbound = w.left + w.width
            for x in xrange(leftbound, rightbound):
                topbound = max(0, w.top - Virtualbot.SIZE[1])
                botbound = w.top + w.height
                for y in xrange(topbound, botbound):
                    self.navbot_reachable[x][y] = False


    def setDestination(self, dest):
        start = (self.body.left, self.body.top)
        if self.navbot_destination == dest:
            return True
        if not self.navbot_reachable[dest[0]][dest[1]]:
            return False
        waypoints = self._construct_waypoints(start, dest)

    def delegateAction(self, status):
        self.setDestination((100, 204))
        pass

    def getAction(self, status):

        self._update_status(status)

        is_ready = self.state == d.action.WAIT

        res = self.delegateAction(status)
        if res:
            return res

        elif is_ready and len(self.navbot_commands) > 0:
            return self.navbot_commands.pop()

        else:
            return {"action": d.action.WAIT}

    """
    Construct an extremely simple waypoint graph out of the arena. The idea is
    to place a "waypoint" every roughly 10 pixels, starting from the bot's
    current position. Ideally this will split the the arena into 10x10 square
    chunks, and when computing a path, the search algorithm will consider
    traversing only these waypoints.
    """
    def _construct_waypoints(self, start, dest):
        # Initialize base waypoint map by floodfilling from start
        waypoints = {}
        """
        q = Queue()
        q.put(start)
        while not q.empty():
            x, y = q.get()
            if (x, y) in waypoints:
                continue
            waypoints[(x, y)] = Navbot.Waypoint(x, y, -1, -1)
            neighbors = []
            waypoints[(x, y)].neighbors = neighbors
            for i in xrange(4):
                next_x = x + d.DC[i]*10
                next_y = y + d.DR[i]*10
                if (next_x < 0 or next_x >= self.arena_body.width or
                    next_y < 0 or next_y >= self.arena_body.height):
                   continue
                neighbors.append((next_x, next_y))
                q.put((next_x, next_y))
        """

        # Extend two axes from dest to connect to waypoint map
        return waypoints
