"""
navbot.py

A base virtualbot class that implements many useful navigation functions
"""

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
        self.navbot_commands = []

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

    def delegateAction(self, status):
        pass

    def getAction(self, status):

        is_ready = status["bot"]["action"] == d.action.WAIT

        res = self.delegateAction(status)
        if res:
            return res

        elif is_ready and len(self.navbot_commands) > 0:
            return self.navbot_commands.pop()

        else:
            return {"action": d.action.WAIT}
