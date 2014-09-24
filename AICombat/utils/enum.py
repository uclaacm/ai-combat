"""
enum.py

A hack to simulate C-style enums.
"""

class Enum(object):

    def __init__(self, *sequential, **named):

        # Basically, creates a dict where the keys are the arguments, and
        # the values are numbers.
        enums = dict(zip(sequential, range(len(sequential))), **named)

        # See attrdict.py for explanation of __dict__
        self.__dict__.update(enums)

    """
    Implements the "in" operator into the more intuitive behavior of checking
    if an item is a valid constant of the enum.
    """
    def __contains__(self, item):
        return item in self.__dict__.values()

    """
    Determines what happens if the object is stringified. For instance, if it's
    being printed.
    """
    def __repr__(self):
        return str(self.__dict__)
