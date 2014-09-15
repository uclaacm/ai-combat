"""
util.py

A file with a bunch of utility functions for collisions and geometry
"""

# Global imports
import pygame
import math
import copy

"""
Infinity constants
"""
POSINF = float("inf")
NEGINF = float("-inf")

"""
IN:  - pygame.Rect
OUT: - 2-tuple representing the center point of the rect
"""
def get_center(rect):
    return (rect.left + rect.width/2, rect.top + rect.height/2)

"""
Scales a rectangle to the new size using the center as pivot
IN:  - pygame.Rect
     - 2-tuple representing new size in (width, height)
OUT: - scaled pygame.Rect
"""
def scale(rect, size):
    new_left = rect.left + rect.width/2 - size[0]/2
    new_top = rect.top + rect.height/2 - size[1]/2
    return pygame.Rect(new_left, new_top, size[0], size[1])

"""
IN:  - 2-tuple representing the 1st point
     - 2-tuple representing the 2nd point
OUT: - float, the distance between the two points
"""
def get_distance(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

"""
Returns the maximum "radius" of the rectangle. This is defined as the radius of
the smallest circle in which the rectangle can be inscribed
IN:  - pygame.Rect
OUT: - float, maximum radius
"""
def get_max_rad(rect):
    topleft = (rect.left, rect.top)
    botright = (rect.left+rect.width, rect.top+rect.height)
    return get_distance(topleft, botright) / 2

"""
Returns the minimum "radius" of the rectangle. This is defined as the radius of the largest circle that can be inscribed in the rectangle
IN:  - pygame.Rect
OUT: - float, minimum radius
"""
def get_min_rad(rect):
    return float(min(rect.width/2, rect.height/2))

"""
Given a rectangle and a circle, determines approximately if they are colliding.
IN:  - pygame.Rect representing the rectangle
     - pygame.Rect representing the circle. The left/top of the rect is
       actually represents the x/y of the center, and height=width=radius
OUT: -
"""
def collide_rect_circle(rect, circle):

    c1 = get_center(rect)
    c2 = (circle.left, circle.top)
    r2 = circle.height

    # Axis-aligned distance check
    dX = abs(c1[0] - c2[0])
    dY = abs(c1[1] - c2[1])
    if dX > rect.width/2 + r2:
        return False
    if dY > rect.height/2 + r2:
        return False

    # Max and min radius distance check
    dist = get_distance(c1, c2)
    if dist > get_max_rad(rect) + r2:
        return False
    if dist < get_min_rad(rect) + r2:
        return True

    # If it gets to this point, besides special configurations, the two objects
    # are probably colliding. In order to be exact, more computationally
    # expensive geometric techniques are required.
    return True

"""
Given an object, a list of obstacles, and the velocity of the object, determines
how far the object can move before hitting any of the obstacles. Note that the
result is only valid for movement along one of the coordinate axes, i.e.
exactly one of vx or vy must be zero.
IN:  - a pygame.Rect representing the object
     - a list of pygame.Rect representing the obstacles
     - a number representing velocity in the x coordinate
     - a number representing velocity in the y coordinate
OUT: - an int representing the max distance the object can travel before
       colliding, or a negative/positive infinity float for no collision
"""
def predict_collision(body, obstacles, vx, vy):
    # Create copies of the object/obstacles so some new utility attributes can
    # be assigned
    b = copy.copy(body)
    b.right = b.left + b.width
    b.bottom = b.top + b.height
    ob = copy.copy(obstacles)
    for o in ob:
        o.right = o.left + o.width
        o.bottom = o.top + o.height

    # The algorithm works almost the same in all four directions, so just define
    # specific configurations for each case
    if vx < 0:
        config = ["max", "left", "right", "top", "bottom"]
    elif vx > 0:
        config = ["min", "right", "left", "top", "bottom"]
    elif vy < 0:
        config = ["max", "top", "bottom", "left", "right"]
    elif vy > 0:
        config = ["min", "bottom", "top", "left", "right"]
    else:
        return 0

    # The time complexity is O(n), n being the number of obstacles. Given that
    # the velocity is along one of the coordinates, collision checking is a few
    # simple bounds check. For instance, if the object is moving right (vx > 0),
    # it will collide with an obstacle if:
    # 1) The y-coordinate of the obstacle's top or bottom wall is between the
    #    object's top and bottom wall, or the converse. This guarantees that
    #    the object will hit the obstacle for some horizontal movement (not
    #    necessarily going right).
    # 2) The x-coordinate of the left wall of the obstacle is greater than the
    #    x-coordinate of the right wall of the object. Thus, by moving right,
    #    the object _will_ hit the obstacle.
    # These conditions are generalized as the perpendicular check and the
    # parallel check. If both of these are satisfied, then the max distance the
    # object can travel is the difference between the obstacle's left wall and
    # the object's right wall.
    limit = NEGINF if config[0] == "max" else POSINF
    for o in obstacles:
        b_perp_tl = getattr(b, config[3])
        b_perp_br = getattr(b, config[4])
        o_perp_tl = getattr(o, config[3])
        o_perp_br = getattr(o, config[4])
        if (b_perp_tl >= o_perp_tl and b_perp_tl < o_perp_br or
            b_perp_br > o_perp_tl and b_perp_br <= o_perp_br or
            b_perp_tl < o_perp_tl and b_perp_br > o_perp_tl):
            b_para_f = getattr(b, config[1])
            o_para_b = getattr(o, config[2])
            if config[0] == "max" and b_para_f >= o_para_b:
                limit = max(limit, o_para_b)
            elif config[0] == "min" and b_para_f <= o_para_b:
                limit = min(limit, o_para_b)

    if limit == NEGINF or limit == POSINF:
        return POSINF
    if config[0] == "max":
        return getattr(b, config[1]) - limit
    else:
        return limit - getattr(b, config[1])
