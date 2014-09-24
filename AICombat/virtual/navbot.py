"""
navbot.py

A virtualbot class that builds on top of Queuebot and implements useful
navigation functions. Subclasses of navbot should interface with it as follows:

For a basic usage of its navigation system, call the navigate() with a
destination parameter, and it will return a list of actions to take to get
there. Alternatively, you can call queue_navigate() to automatically add the
actions into the Queuebot queue (see documentation on how Queuebot works). The
navigate function also supports a start and direction parameters if you don't
want to use the bot's current location and direction.

Usually you will want to retain control of the bot while it's navigating to a
destination. In this case, you must enable preemption on Queuebot, and monitor
the status of the queue yourself. Note that if you interrupt a navigation
action sequence to perform an action, most of the time your navigation sequence
will be invalidated (for instance, you suddenly decide to turn around, or
prematurely cancel a long walk), and you must clear the queue and re-navigate.
"""

# Global imports
import copy
import heapq

# Local imports
import real.definitions as d
from virtual.queuebot import Queuebot
from utils.comparable import Comparable

class Navbot(Queuebot):

    """
    A utility Waypoint class that defines nodes in the map for path-finding.
    These Waypoints support a heuristic and distance for use by A*, a prev
    variable for tracking path, and a direction marker to account for turn rate.
    """
    class Waypoint(Comparable):

        def __init__(self, x, y, heuristic, distance, prev, direction):
            self.x = x
            self.y = y
            self.heuristic = heuristic
            self.distance = distance
            self.priority = self.heuristic + self.distance
            self.prev = prev
            self.direction = direction

        """
        Mandatory override of the < operator for Comparable
        """
        def __lt__(self, other):
            if self.priority != other.priority:
                return self.priority < other.priority
            if self.heuristic != other.heuristic:
                return self.heuristic < other.heuristic
            return (self.x, self.y) < (other.x, other.y)

    def __init__(self, arena_data):

        # Initialization
        Queuebot.__init__(self, arena_data)
        self.image_path = "img/navbot.png"

        # Navbot stuff
        self.navbot_waypoints = []
        self.navbot_reachable = []

        # Compute all reachable and unreachable pixels
        # Won't use _too_ much memory as long as the map isn't too big....
        # Allows O(1) path collision detection instead of O(len(walls))
        # Also allows easier construction of waypoint grid during path finding
        for x in xrange(self.arena.height):
            self.navbot_reachable.append([True] * self.arena.width)
        for w in self.walls:
            leftbound = max(0, w.left - self.body.width + 1)
            rightbound = w.left + w.width
            for x in xrange(leftbound, rightbound):
                topbound = max(0, w.top - self.body.height + 1)
                botbound = w.top + w.height
                for y in xrange(topbound, botbound):
                    self.navbot_reachable[x][y] = False

    """
    Computes an action sequence that will bring the bot from its current
    position to the specified destination.
    IN:  - tuple of (x, y) specifying destination
    OUT: - a list of actions to take, or None to mean that it is impossible to
           reach that destination
    """
    def navigate(self, dest, start=None, direction=None):

        # Initialize parameters if not given
        if start is None:
            start = self.get_location()
        if direction is None:
            direction = self.direction

        # Perform basic feasibility checks
        if direction not in d.direction:
            return None
        if not self.arena.collidepoint(start):
            return None
        if not self.arena.collidepoint(dest):
            return None
        if not self.navbot_reachable[start[0]][start[1]]:
            return None
        if not self.navbot_reachable[dest[0]][dest[1]]:
            return None
        if start == dest:
            return []

        # Find a path of waypoints to destination
        path = self._find_path(start, dest, direction)
        if not path:
            return None

        # Construct command queue from path
        return self._construct_commands(path)

    """
    An extra queue method to supplement existing Queuebot primitives. This
    function simply retrieves a list of actions required to navigate to dest,
    and adds them to the queue.
    IN:  - tuple of (x, y) specifying destination
    OUT: - bool indicating whether a path was successfully found and queued
    """
    def queue_navigate(self, dest):
        actions = self.navigate(dest)
        if actions is None:
            return False
        self.queue_all(actions)
        return True

    """
    Main entry point from realbot into the navbot, overridden from virtualbot.
    Updates status and asks subclasses for an action. Manages the command
    sequence when during navigation. If you want full control over the navbot,
    override this function. Overriding this function invalidates
    delgate_action()
    IN:  - realbot status
    OUT: - dict specifying action to take
    """
    @Queuebot.queued
    def get_action(self, status):
        # Here's a demo of how navigate can be used
        checkpoints = [(250, 100),
                       (0, 0),
                       (360, 0),
                       (11, 136),
                       (325, 225)]
        for i in xrange(len(checkpoints)-1):
            if self.get_location() == checkpoints[i]:
                self.queue_navigate(checkpoints[i+1])

    """
    Private function that takes a path of waypoints and converts it into a
    series of actions to take.
    """
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
            move_dir = self._calculate_direction(prev, cur)
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
        return commands

    """
    OUT: - tuple representing the bot's position as (x, y)
    """
    def get_location(self):
        return (self.body.left, self.body.top)

    """
    Calculates the direction pointing from start to dest. If the result turns
    IN:  - tuple indicating start point
         - tuple indicating destination point
    OUT: - direction from start to dest, -1 if not a defined direction
    """
    def _calculate_direction(self, start, dest):
        x_diff = dest[0] - start[0]
        y_diff = dest[1] - start[1]
        if not y_diff:
            if x_diff > 0:
                return d.direction.RIGHT
            elif x_diff < 0:
                return d.direction.LEFT
        if not x_diff:
            if y_diff > 0:
                return d.direction.DOWN
            elif y_diff < 0:
                return d.direction.UP
        return -1

    """
    Computes a path to the destination by applying A* on an extremely simple
    waypoint grid. The idea is to walk to a "waypoint" every 10 pixels, starting
    from the bot's current position. Ideally this will split the arena into
    10x10 square chunks, and when computing a path, the search algorithm will
    consider traversing only these waypoints.
    IN:  - tuple indicating start point
         - tuple indicating destination point
    OUT: - list containing points to follow to get to destination
    """
    def _find_path(self, start, dest, direction):

        # These difference offsets are used to place intermediate waypoints on
        # the axes of the destination
        x_diff = (dest[0]-start[0]) % 10
        y_diff = (dest[1]-start[1]) % 10

        # targets is a min-heap that contains candidate waypoints for visiting
        targets = []
        heapq.heappush(targets, Navbot.Waypoint(start[0], start[1], self._heuristic(start, dest), 0, None, direction))

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
                if (next_x < 0 or next_x >= self.arena.width or
                    next_y < 0 or next_y >= self.arena.height or
                    not self.navbot_reachable[next_x][next_y] or
                    next_cur in waypoints):
                    continue

                # Compute cost to get there
                cost = wp.distance
                cost += (abs(x_off) + abs(y_off)) * d.duration.WALK
                diff_dir = (wp.direction - i) % 4
                if diff_dir == 1 or diff_dir == 3:
                    cost += d.duration.TURN
                elif diff_dir == 2:
                    cost += d.duration.TURN * 2

                # Save as candidate location to visit
                next_wp = Navbot.Waypoint(next_x, next_y, self._heuristic(next_cur, dest), cost, cur, i)
                waypoints[next_cur] = next_wp
                heapq.heappush(targets, next_wp)

        # If a path is not found
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

    """
    The heuristic for A*. Simply the Manhattan distance divided by speed.
    """
    def _heuristic(self, loc, dest):
        return (abs(loc[0]-dest[0]) + abs(loc[1]-dest[1])) * d.duration.WALK

    """
    Utility function to determine if loc is between base and base+offset
    """
    def _between(self, loc, base, offset):
        return (loc < base and loc > base+offset or
                loc > base and loc < base+offset)

    """
    Computes how far in the x-y direction to move for the next waypoint. The
    ugly if statement accounts for intermediate waypoints that are on the
    destination point's axes (because the destination is rarely a multiple of
    10 pixels distance from start).
    """
    def _compute_offsets(self, cur, dest, direction, x_diff, y_diff):
        x_off = d.DX[direction] * 10
        y_off = d.DY[direction] * 10
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
