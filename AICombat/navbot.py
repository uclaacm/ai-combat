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

        def __init__(self, x, y, h, d, p):
            self.x = x
            self.y = y
            self.heuristic = h
            self.distance = d
            self.priority = h + d
            self.prev = p

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


    """
    Computes a path to the destination by applying A* on an extremely simple
    waypoint grid. The idea is to walk to a "waypoint" every 10 pixels, starting
    from the bot's current position. Ideally this will split the arena into
    10x10 square chunks, and when computing a path, the search algorithm will
    consider traversing only these waypoints.
    """
    def setDestination(self, dest):
        start = (self.body.left, self.body.top)

        # Perform basic feasibility checks
        if self.navbot_destination == dest:
            return True
        if not self.navbot_reachable[dest[0]][dest[1]]:
            return False

        # The path finding algorithm
        # These offsets are used for place intermediate waypoints on the
        # axes of the destination
        x_offset = (start[0]-dest[0]) % 10
        y_offset = (start[1]-dest[1]) % 10
        # targets contain candidate waypoints for visiting
        targets = {}
        targets[start] = Navbot.Waypoint(start[0], start[1], self._heuristic(start, dest), 0, None)
        # waypoints save information about each visited waypoint
        waypoints = {}
        while targets:
            # Look for the waypoint closest to destination
            wp = None
            for w in targets.itervalues():
                if (not wp or w.priority < wp.priority or
                    w.priority == wp.priority and w.heuristic < wp.heuristic):
                    wp = w
            loc = (wp.x, wp.y)
            targets.pop(loc)
            waypoints[loc] = wp
            # Uncomment line below to see how A* searches
            # raw_input("{0} {1} {2}".format(loc, wp.priority, wp.heuristic))
            if loc == dest:
                break
            for i in xrange(4):
                # Ugly if conditions to account for intermediate waypoints
                xmod = 0
                ymod = 0
                if i == 0:
                    if wp.x == dest[0]: xmod = x_offset
                    elif self._between(dest[0], wp.x, 10): xmod = 10-x_offset
                    else: xmod = 10
                elif i == 1:
                    if wp.y == dest[1]: ymod = y_offset
                    elif self._between(dest[1], wp.y, 10): ymod = 10-y_offset
                    else: ymod = 10
                if i == 2:
                    if wp.x == dest[0]: xmod = x_offset-10
                    elif self._between(dest[0], wp.x, 10): xmod = -x_offset
                    else: xmod = -10
                elif i == 3:
                    if wp.y == dest[1]: ymod = y_offset-10
                    elif self._between(dest[1], wp.y, 10): ymod = -y_offset
                    else: ymod = -10
                next_x = wp.x + xmod
                next_y = wp.y + ymod
                next_loc = (next_x, next_y)
                # Make sure next location is legal, reachable, and unvisited
                if (next_x < 0 or next_x >= self.arena_body.width or
                    next_y < 0 or next_y >= self.arena_body.height or
                    not self.navbot_reachable[next_x][next_y] or
                    next_loc in waypoints):
                    continue
                targets[next_loc] = Navbot.Waypoint(next_x, next_y, self._heuristic(next_loc, dest), wp.distance + abs(xmod) + abs(ymod), loc)

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


    def _heuristic(self, loc, dest):
        return abs(loc[0]-dest[0]) + abs(loc[1]-dest[1])

    def _between(self, loc, base, offset):
        return (loc < base and loc > base+offset or
                loc > base and loc < base+offset)
