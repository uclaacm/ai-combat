"""
attrdict.py

Uses a hack to generate clean, attribute-indexable dictionaries.
e.g. object.value as opposed to object["value"]
"""

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        # __dict__ is a special built-in dict in Python objects for accessing
        # user-defined attributes. When you call object.value, you're really
        # calling object.__dict__["value"]. What happens when you do
        # object.__dict__["__dict__"]? Cython at least (the Python interpreter
        # that most people use by default) says that doesn't exist, since
        # __dict__ exists only within the interpreter
        self.__dict__ = self
