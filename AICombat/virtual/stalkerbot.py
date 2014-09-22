"""
stalkerbot.py

An aggressive virtualbot that wanders around the arena searching for enemy
bots. Upon finding an enemy, the stalkerbot will chase after and attack it
until either it or its target is dead (or the target goes out of sight).

Stalkerbot uses Navbot to navigate and chase.
"""

# Global imports
import random

# Local imports
import real.definitions as d
import utils.geometry as g
from real.bullet import Bullet
from virtual.navbot import Navbot

class Stalkerbot(Navbot):

    def __init__(self, arena_data):

        # Initialization
        Navbot.__init__(self, arena_data)
        self.image_path = "img/stalkerbot.png"

        # Stalkerbot stuff
        self.target = None
        ### A lambda is just a tiny, anonymous in-line function. In this case,
        ### it's used as an alias to produce a random cooldown value
        self.shoot_cooldown = lambda: random.randint(5,15)
        self.shoot_counter = 0
        self.search_cooldown = lambda: random.randint(3,7)
        self.search_counter = 0

    """
    Reset variables and choose a new target to stalk
    """
    def switch_target(self, enemies):
        self.shoot_counter = 0
        self.search_counter = 0
        return random.choice(enemies)

    """
    Overridden from Navbot. Most of the time, Stalkerbot is navigating to a
    specific point in the arena, which it lets Navbot handle. However, if it's
    stalking an enemy, it will shoot (respecting a shoot cooldown) every time
    the enemy comes within firing range. Stalkerbot periodically updates its
    target's position (respecting a search cooldown).
    """
    def delegate_action(self, status):

        # Cool down
        self.shoot_counter -= 1
        self.search_counter -= 1

        enemies = status["objects"]["bots"]
        if enemies:

            # Get valid target, whether it's making sure the current target is
            # still here, or selecting a new target
            if not self.target:
                self.target = self.switch_target(enemies)
            else:
                t = [e for e in enemies if e["eid"] == self.target["eid"]]
                if not t:
                    self.target = self.switch_target(enemies)
                else:
                    self.target = t[0]

            # See if it can shoot the target
            if self.shoot_counter <= 0 and self.can_hit(self.target["body"]):
                self.shoot_counter = self.shoot_cooldown()
                self.search_counter = 0
                return {"action": d.action.SHOOT}

            # Periodically update target coordinates
            if self.search_counter <= 0:
                self.search_counter = self.search_cooldown()
                target_loc = (self.target["body"].left, self.target["body"].top)
                self.set_destination(target_loc)

        else:

            # Wander around the arena to look for a target
            while not self.get_destination():
                x = random.randrange(self.arena.width)
                y = random.randrange(self.arena.height)
                self.set_destination((x, y))

    """
    Given a target's position, this method determines whether a bullet shot by
    the Stalkerbot will strike the target.
    IN:  - pygame.Rect representing the target's position
    OUT: - bool indicating the bullet can hit or not
    """
    def can_hit(self, body):

        # Simulate bullet collision trajectory with target
        bullet_body = g.scale(self.body, Bullet.SIZE)
        body_distance = g.predict_collision(bullet_body,
                                            [body],
                                            d.DX[self.direction],
                                            d.DY[self.direction])
        if body_distance == g.POSINF:
            return False

        # Simulate bullet collision trajectory with walls
        block_distance = g.predict_collision(bullet_body,
                                             self.walls,
                                             d.DX[self.direction],
                                             d.DY[self.direction])
        if block_distance < body_distance:
            return False

        return True

