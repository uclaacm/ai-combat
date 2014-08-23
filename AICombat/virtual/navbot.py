"""
from virtual.dumbbot import Dumbbot
navbot.py

A base virtualbot class that implements many useful navigation functions
"""

# Global imports
import pygame
import copy
import heapq

# Local imports
import real.definitions as d
from virtual.virtualbot import Virtualbot
from utils.comparable import Comparable

class Navbot(Virtualbot):

    class Waypoint(Comparable):

        def __init__(self, x, y, heuristic, distance, prev, direction):
            self.x = x
            self.y = y
            self.heuristic = heuristic
            self.distance = distance
            self.priority = self.heuristic + self.distance
            self.prev = prev
            self.direction = direction

        def __lt__(self, other):
            if self.priority != other.priority:
                return self.priority < other.priority
            if self.heuristic != other.heuristic:
                return self.heuristic < other.heuristic
            return (self.x, self.y) < (other.x, other.y)

    def __init__(self, arena_data):

        Virtualbot.__init__(self, arena_data)
        self.image_path = "img/navbot.png"

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

    def set_destination(self, dest):
        start = self.get_location()

        # Perform basic feasibility checks
        if not self.arena_body.collidepoint(dest):
            return False
        if dest == self.navbot_destination or dest == start:
            return True
        if not self.navbot_reachable[dest[0]][dest[1]]:
            return False

        # Find a path of waypoints to destination
        path = self._find_path(start, dest)
        if not path:
            return False

        # Construct command queue from path
        self.navbot_commands = self._construct_commands(path)

        self.navbot_destination = dest

        return True

    def delegate_action(self, status):
        # Temporary demo of navigation
        checkpoints = [(250, 100),
                       (0, 0),
                       (360, 0),
                       (11, 136),
                       (211, 321)]
        if not self.navbot_destination:
            for i in xrange(len(checkpoints)-1):
                if self.get_location() == checkpoints[i]:
                    self.set_destination(checkpoints[i+1])

    def get_action(self, status):

        self._update_status(status)

        is_ready = self.state['action'] == d.action.WAIT

        res = self.delegate_action(status)
        if res:
            return res

        elif is_ready and len(self.navbot_commands) > 0:
            c = self.navbot_commands.pop()
            if not self.navbot_commands:
                self.navbot_destination = None
            return c
        else:
            return {"action": d.action.CONTINUE}

    def _construct_commands(self, path):
        LEFT_TURN = {"action": d.action.TURN,
                     "direction": d.direction.LEFT}
        RIGHT_TURN = {"action": d.action.TURN,
                     "direction": d.direction.RIGHT}
        WALK = {"action": d.action.WALK}

        commands = []
        prev = path[0]
        cur_dir = self.direction
        for i in xrange(1, len(path)):
            cur = path[i]
            move_dir = self._get_direction(prev, cur)
            diff = move_dir - cur_dir
            if diff % 4 == 1:
                commands.append(LEFT_TURN)
            elif diff % 4 == 2:
                commands.append(RIGHT_TURN)
                commands.append(RIGHT_TURN)
            elif diff % 4 == 3:
                commands.append(RIGHT_TURN)
            cur_dir = move_dir
            dist = abs(prev[0]-cur[0]) + abs(prev[1]-cur[1])
            if diff == 0 and commands:
                commands[-1]["distance"] += dist
            else:
                WALK["distance"] = dist
                commands.append(copy.copy(WALK))
            prev = cur
        commands.reverse()
        return commands

    def get_location(self):
        return (self.body.left, self.body.top)

    def _get_direction(self, start, dest):
        x_diff = dest[0] - start[0]
        y_diff = dest[1] - start[1]
        if not y_diff:
            if x_diff > 0:
                return 0
            elif x_diff < 0:
                return 2
        if not x_diff:
            if y_diff > 0:
                return 3
            elif y_diff < 0:
                return 1
        return 5

    """
    Computes a path to the destination by applying A* on an extremely simple
    waypoint grid. The idea is to walk to a "waypoint" every 10 pixels, starting
    from the bot's current position. Ideally this will split the arena into
    10x10 square chunks, and when computing a path, the search algorithm will
    consider traversing only these waypoints.
    IN:  - tuple indicating start point
         - tuple indicating end point
    OUT: - list containing points to follow to get to destination
    """
    def _find_path(self, start, dest):

        # These difference offsets are used to place intermediate waypoints on
        # the axes of the destination
        x_diff = (dest[0]-start[0]) % 10
        y_diff = (dest[1]-start[1]) % 10

        # targets is a min-heap that contains candidate waypoints for visiting
        targets = []
        heapq.heappush(targets, Navbot.Waypoint(start[0], start[1], self._heuristic(start, dest), 0, None, self.direction))

        # waypoints save information about each visited waypoint
        waypoints = {}
        waypoints[start] = targets[0]
        while targets:

            # Look for the waypoint closest to destination
            wp = heapq.heappop(targets)
            cur = (wp.x, wp.y)

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

                # Make sure next location is legal, reachable, and unseen
                if (next_x < 0 or next_x >= self.arena_body.width or
                    next_y < 0 or next_y >= self.arena_body.height or
                    not self.navbot_reachable[next_x][next_y] or
                    next_cur in waypoints):
                    continue

                cost = wp.distance
                cost += (abs(x_off) + abs(y_off)) * d.duration.WALK
                diff_dir = (wp.direction - i) % 4
                if diff_dir == 1 or diff_dir == 3:
                    cost += d.duration.TURN
                elif diff_dir == 2:
                    cost += d.duration.TURN * 2

                next_wp = Navbot.Waypoint(next_x, next_y, self._heuristic(next_cur, dest), cost, cur, i)
                waypoints[next_cur] = next_wp
                heapq.heappush(targets, next_wp)

        # If path is not found
        if dest not in waypoints:
            return []

        # Retrieve path of waypoints
        loc = dest
        path = []
        while loc:
            path.append(loc)
            loc = waypoints[loc].prev
        path.reverse()

        return path


    def _heuristic(self, loc, dest):
        return (abs(loc[0]-dest[0]) + abs(loc[1]-dest[1])) * d.duration.WALK

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
                x_off = 10-x_diff
            elif self._between(dest[0], cur[0], 10):
                x_off = x_diff
        elif direction == 1:
            if cur[1] == dest[1]:
                y_off = -y_diff
            elif self._between(dest[1], cur[1], -10):
                y_off = y_diff-10
        elif direction == 2:
            if cur[0] == dest[0]:
                x_off = -x_diff
            elif self._between(dest[0], cur[0], -10):
                x_off = x_diff-10
        elif direction == 3:
            if cur[1] == dest[1]:
                y_off = 10-y_diff
            elif self._between(dest[1], cur[1], 10):
                y_off = y_diff
        return (x_off, y_off)
