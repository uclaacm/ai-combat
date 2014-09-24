"""
comparable.py

An abstract base class (i.e. a class with a partial implementation that
subclasses are required to finish) that allows subclasses to easily implement a
custom comparison operator.
"""

class Comparable(object):

    """
    This function works as the less than operator. All other operators are
    based off of this.
    """
    def __lt__(self, other):
        raise NotImplementedError("__lt__ must be overloaded for Comparable")

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self
