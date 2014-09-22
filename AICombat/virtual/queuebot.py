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
        self.queue_actions = deque()
        self.queue_preempt = False
        self.queue_cleared = False

    """
    A decorator for get_action. By default, get_action is somewhat unwieldy to
    use because it is required to return single primitive actions. This is
    somewhat nice for flexibility, but at the cost of developer-unfriendliness.
    This decorator uses a queue_actions to save primitives and returns them in
    sequence, only calling get_action if the queue is exhausted. A subclass can
    then choose to push actions into the queue, and/or return a primitive. If
    a primitive is returned, it is given priority over anything in the queue.
    """
    @staticmethod
    def queued(func):

        def decorated(self, status):

            # Save status updates
            self.update_status(status)

            # Initialize state variables
            ready = self.state['action'] == d.action.WAIT

            # Preemption mode (see description for preempt_queue())
            if self.queue_preempt:
                self.queue_cleared = False
                ### Ask subclass for an explicit action
                ret = func(self, status)
                if ret:
                    return ret
                ### Realbot still performing an action
                if not ready and not self.queue_cleared:
                    return {"action": d.action.CONTINUE}
                ### There actions left in the queue
                if self.queue_actions:
                    return self.queue_actions.popleft()
                ### Subclass cleared the queue
                if self.queue_cleared:
                    return {"action": d.action.WAIT}

            # Normal mode
            else:
                ### Realbot still performing an action
                if not ready:
                    return {"action": d.action.CONTINUE}
                ### There are actions left in the queue
                if self.queue_actions:
                    return self.queue_actions.popleft()
                ### Ask subclass for an explicit action
                ret = func(self, status)
                if ret:
                    return ret
                ### Now there are actions left in the queue
                if self.queue_actions:
                    return self.queue_actions.popleft()

            # No other conditions are satisfied
            return {"action": d.action.CONTINUE}

        return decorated

    """
    Used by a subclass to tell Queuebot that it wants to preempt the queue.
    What this means is that, instead of executing every action in the queue
    before asking the subclass for more actions, the Queuebot will now always
    ask for new actions before executing its queue. This allows bots to
    continue monitoring their status while executing an action sequence.
    """
    def preempt_queue(self, value=True):
        self.queue_preempt = value

    """
    Lets subclasses know if the queue is empty. Useful during preemption mode.
    """
    def is_queue_empty(self):
        return len(self.queue_actions) == 0

    """
    Clears the queue of actions. If the bot is currently executing an action
    (e.g. walk), it will also be canceled. Useful during preemption mode.
    """
    def clear_queue(self):
        self.queue_actions = deque()
        self.queue_cleared = True

    def queue_left(self):
        a = {"action": d.action.TURN,
             "direction": d.direction.LEFT}
        self.queue_actions.append(a)

    def queue_right(self):
        a = {"action": d.action.TURN,
             "direction": d.direction.RIGHT}
        self.queue_actions.append(a)

    def queue_wait(self):
        a = {"action": d.action.WAIT}
        self.queue_actions.append(a)

    def queue_continue(self):
        a = {"action": d.action.CONTINUE}
        self.queue_actions.append(a)

    def queue_walk(self, distance=None):
        if distance is None:
            distance = self.step
        a = {"action": d.action.WALK,
             "distance": distance}
        self.queue_actions.append(a)

    def queue_shoot(self):
        a = {"action": d.action.SHOOT}
        self.queue_actions.append(a)

    def queue_reverse(self):
        self.queue_left()
        self.queue_left()

    def queue_all(self, actions):
        self.queue_actions.extend(actions)
