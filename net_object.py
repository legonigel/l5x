'''
Created on Nov 2, 2015

@author: "hutcheb"
'''

from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement)
import ctypes
from .tag import Tag

class FBD_Object(ElementAccess):
    """Abstract class for fbdObjects"""
    x = AttributeDescriptor('X', True)   
    y = AttributeDescriptor('Y', True) 
   
class FBD_IRef(FBD_Object):
    """Base class for a single IRef""" 
    operand = AttributeDescriptor('Operand', True)  
    hide_desc = AttributeDescriptor('HideDesc', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)

class FBD_ORef(FBD_Object):
    """Base class for a single ORef""" 
    operand = AttributeDescriptor('Operand', True)  
    hide_desc = AttributeDescriptor('HideDesc', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        
class FBD_TextBox(FBD_Object):
    """Base class for a single Textbox""" 
    text = ElementDescription([], 'Text')
    width = AttributeDescriptor('Width', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        
class FBD_Default(FBD_Object):
    """Default class for any block that can't be found""" 

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        
class Wire(ElementAccess):
    """Base class for a wire""" 
    text = ElementDescription([], 'Text')
    fromID = AttributeDescriptor('FromID', True)  
    toID = AttributeDescriptor('ToID', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)
    