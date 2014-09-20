"""
queuebot.py

A pure utility virtualbot to be subclassed. The Queuebot provides a queue
decorator to be used on get_action, allowing subclasses to define action
sequences instead of juggling around action primitives.
"""

# Global imports
from collections import deque

# Local imports
import real.definitions as d
from virtual.virtualbot import Virtualbot

class Queuebot(Virtualbot):

    def __init__(self, arena_data):

        # Initialization
        Virtualbot.__init__(self, arena_data)
        
        # Queuebot stuff
        self.command_queue = deque()

    """
    A decorator for get_action. By default, get_action is somewhat unwieldy to
    use because it is required to return single primitive actions. This is
    somewhat nice for flexibility, but at the cost of developer-unfriendliness.
    This decorator uses a command_queue to save primitives and returns them in
    sequence, only calling get_action if the queue is exhausted. A subclass can
    then choose to push actions into the queue, and/or return a primitive. If
    a primitive is returned, it is given priority over anything in the queue.
    """
    def queue(func):
        def decorated(self, status):
            if self.command_queue:
                return self.command_queue.popleft()
            ret = func(self, status)
            if ret:
                return ret
            if self.command_queue:
                return self.command_queue.popleft()
            return {"action": d.action.CONTINUE}
        return decorated

    def queue_left(self):
        a = {"action": d.action.TURN,
             "direction": d.direction.LEFT}
        self.command_queue.append(a)
        
    def queue_right(self):
        a = {"action": d.action.TURN,
             "direction": d.direction.RIGHT}
        self.command_queue.append(a)
        
    def queue_wait(self):
        a = {"action": d.action.WAIT}
        self.command_queue.append(a)
        
    def queue_continue(self):
        a = {"action": d.action.CONTINUE}
        self.command_queue.append(a)
        
    def queue_walk(self, distance=999999):
        a = {"action": d.action.WALK,
             "distance": distance}
        self.command_queue.append(a)
        
    def queue_shoot(self):
        a = {"action": d.action.SHOOT}
        self.command_queue.append(a)
        
    def queue_reverse(self):
        self.queue_left()
        self.queue_left()
        
    def queue_actions(self, actions):
        sef.command_queue.extend(actions)