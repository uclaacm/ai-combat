"""
enum.py

A hack to simulate C-style enums.
"""

class Enum(object):

    def __init__(self, *sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        self.__dict__.update(enums)

    def __contains__(self, item):
        return item in self.__dict__.values()

    def __repr__(self):
        return str(self.__dict__)
