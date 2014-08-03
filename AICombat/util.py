"""
util.py

A file with a bunch of utility functions for collisions and geometry
"""

# Global imports
import pygame

"""
Given a pygame.Rect, returns its center point as a 2-tuple
"""
def get_center(rect):
    return (rect.left + rect.width/2, rect.top + rect.height/2)

"""
Given two points, find the distance between them
"""
def get_distance(pt1, pt2):
    return pt1[0]
