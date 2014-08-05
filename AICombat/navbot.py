"""
navbot.py

A base virtualbot class that implements many useful navigation functions
"""

# Global imports
from collections import deque

# Local imports
import definitions as d
from virtualbot import Virtualbot

class Navbot(Virtualbot):

    class Waypoint():
        
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.neighbors = []

    def __init__(self, arena_data):
        Virtualbot.__init__(self, arena_data)
        self.imagePath = "navbot.png"

        # Declare navbot internals
        self.navbot_destination = None
        self.navbot_waypoints = []
        self.command_queue = deque()

        # Save arena layout
        self.arena_body = pygame.Rect(0, 0, arena_data["width"], arena_data["height"])
        self.arean_walls = arena_data["walls"]

        # Construct an extremely simple waypoint graph out of the arena. The
        # idea is to place a "waypoint" every 10 pixels. Ideally this will
        # split the the arena into 10x10 square chunks, and when computing a
        # path, the search algorithm will consider traversing only these
        # waypoints.
        for x in xrange(0, self.arena_body.width-20, 10):
            self.navbot_waypoints.append([])
            for y in xrange(0, self.arena_body.height-20, 10):
                self.navbot_waypoints[-1].append(Waypoint(x, y))

    def setDestination(self, dest):
        if self.navbot_destination == dest:
            return
        x, y = dest

    def getAction(self, status):

        is_ready = status["bot"]["action"] == d.action.WAIT

        if "navbot_delegate" in dir(self):
            res = self.navbot_delegate(objects, time)
            if res:
                return res

        if is_ready and len(self.command_queue) > 0:
            return self.command_queue.popleft()

        decision = {}
        decision['action'] = d.action.WAIT

        return decision
