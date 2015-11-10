'''
Created on Nov 4, 2015

@author: "hutcheb"
'''

class InvalidFile(Exception):
    """Raised if the given .L5X file was not a proper L5X export."""
    pass

class RungNumberOutOfRangeError(Exception):
    """Raised if the given rung number is out of range"""
    pass

class SheetNumberOutOfRangeError(Exception):
    """Raised if the given sheet number is out of range"""
    pass
