"""
stalkerbot.py
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
        ### How many frames to wait before shooting again
        self.shoot_cooldown = lambda: random.randint(5,15)
        self.shoot_counter = 0
        ### How many frames to wait before computing path to target again
        self.search_cooldown = lambda: random.randint(5,10)
        self.search_counter = 0

    def switch_target(self, enemies):
        self.shoot_counter = 0
        self.search_counter = 0
        return random.choice(enemies)

    def delegate_action(self, status):

        self.shoot_counter -= 1
        self.search_counter -= 1

        enemies = status["objects"]["bots"]
        if enemies:

            # Get valid target
            if not self.target:
                self.target = self.switch_target(enemies)
            else:
                t = [e for e in enemies if e["eid"] == self.target["eid"]]
                if not t:
                    self.target = self.switch_target(enemies)
                else:
                    self.target = t[0]

            # See if you can shoot the target
            if self.shoot_counter <= 0 and self.can_hit(self.target["body"]):
                self.shoot_counter = self.shoot_cooldown()
                self.search_counter = 0
                return {"action": d.action.SHOOT}

            if self.search_counter <= 0:
                self.search_counter = self.search_cooldown()
                target_loc = (self.target["body"].left, self.target["body"].top)
                self.set_destination(target_loc)

        else:

            while not self.get_destination():
                x = random.randrange(self.arena_body.width)
                y = random.randrange(self.arena_body.height)
                self.set_destination((x, y))

    def can_hit(self, body):
        bullet_body = g.scale(self.body, Bullet.SIZE)
        body_distance = g.predict_collision(bullet_body,
                                            [body],
                                            d.DX[self.direction],
                                            d.DY[self.direction])
        if body_distance == g.POSINF:
            return False
        walls = [w.body for w in self.get_walls()]
        block_distance = g.predict_collision(bullet_body,
                                             walls,
                                             d.DX[self.direction],
                                             d.DY[self.direction])
        if block_distance < body_distance:
            return False
        return True

