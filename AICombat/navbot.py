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

        def __init__(self, x, y, heuristic, distance, prev):
            self.x = x
            self.y = y
            self.heuristic = heuristic
            self.distance = distance
            self.priority = heuristic + distance
            self.prev = prev

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
        # These difference offsets are used to place intermediate waypoints on
        # the axes of the destination
        x_diff = (start[0]-dest[0]) % 10
        y_diff = (start[1]-dest[1]) % 10
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
            cur = (wp.x, wp.y)
            targets.pop(cur)
            waypoints[cur] = wp
            # Uncomment line below to see how A* searches
            # raw_input("{0} {1} {2}".format(cur, wp.priority, wp.heuristic))
            if cur == dest:
                break
            for i in xrange(4):
                # Determine how to move
                x_off, y_off = self._compute_offsets(cur, dest, i, x_diff, y_diff)
                next_x = wp.x + x_off
                next_y = wp.y + y_off
                next_cur = (next_x, next_y)
                # Make sure next location is legal, reachable, and unvisited
                if (next_x < 0 or next_x >= self.arena_body.width or
                    next_y < 0 or next_y >= self.arena_body.height or
                    not self.navbot_reachable[next_x][next_y] or
                    next_cur in waypoints):
                    continue
                targets[next_cur] = Navbot.Waypoint(next_x, next_y, self._heuristic(next_cur, dest), wp.distance + abs(x_off) + abs(y_off), cur)

    def delegateAction(self, status):
        self.setDestination((100, 204))

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

    def _compute_offsets(self, cur, dest, direction, x_diff, y_diff):
        # This ugly if structure accounts for intermediate waypoints on the axes
        # of the destination. There must be waypoints on the axes or else the
        # bot cannot reach the destination.
        x_off = d.DC[direction] * 10
        y_off = d.DR[direction] * 10
        if direction == 0:
            if cur[0] == dest[0]:
                x_off = x_diff
            elif self._between(dest[0], cur[0], 10):
                x_off = 10-x_diff
        elif direction == 1:
            if cur[1] == dest[1]:
                y_off = y_diff
            elif self._between(dest[1], cur[1], 10):
                y_off = 10-y_diff
        elif direction == 2:
            if cur[0] == dest[0]:
                x_off = x_diff-10
            elif self._between(dest[0], cur[0], 10):
                x_off = -x_diff
        elif direction == 3:
            if cur[1] == dest[1]:
                y_off = y_diff-10
            elif self._between(dest[1], cur[1], 10):
                y_off = -y_diff
        return (x_off, y_off)
