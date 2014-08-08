"""
util.py

A file with a bunch of utility functions for collisions and geometry
"""

# Global imports
import pygame
import math

"""
IN:  - pygame.Rect
OUT: - 2-tuple representing the center point of the rect
"""
def get_center(rect):
    return (rect.left + rect.width/2, rect.top + rect.height/2)

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
    if (dX > rect.width/2 + r2):
        return False
    if (dY > rect.height/2 + r2):
        return False

    # Max and min radius distance check
    dist = get_distance(c1, c2)
    if (dist > get_max_rad(rect) + r2):
        return False
    if (dist < get_min_rad(rect) + r2):
        return True

    # If it gets to this point, besides special configurations, the two objects
    # are probably colliding. In order to be exact, more computationally
    # expensive geometric techniques are required.
    return True
