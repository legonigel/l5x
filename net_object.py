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
    x = AttributeDescriptor('X', False)   
    y = AttributeDescriptor('Y', False) 
    ID = AttributeDescriptor('ID', False) 
    
    @classmethod
    def create(cls, parent, block_type, attributes={}):
        """Get the last unused ID"""
        type_dict = {
           'IRef': FBD_IRef,
           'ORef': FBD_ORef,
           'TextBox': FBD_TextBox}
        ID = 0
        for key in parent.blocks:            
            if ID <= int(key):
                ID = 1 + int(key)        
        attributes.update({'ID' : str(ID)})
        element = parent._create_append_element(parent.element, \
                                             block_type, \
                                             attributes)
        new = type_dict[block_type](element)       
        parent.blocks.append(str(ID), new.element)
        return new  
   
class FBD_IRef(FBD_Object):
    """Base class for a single IRef""" 
    operand = AttributeDescriptor('Operand', True)  
    hide_desc = AttributeDescriptor('HideDesc', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)

    @classmethod
    def create(cls, parent, operand, x=0, y=0):
        new = FBD_Object.create(parent, 'IRef', {'Operand' : operand, \
                                          'X' : str(x),
                                          'Y' : str(y),
                                          'HideDesc' : 'false'})
        return new

class FBD_ORef(FBD_Object):
    """Base class for a single ORef""" 
    operand = AttributeDescriptor('Operand', True)  
    hide_desc = AttributeDescriptor('HideDesc', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)

    @classmethod
    def create(cls, parent, operand, x=0, y=0):
        new = FBD_Object.create(parent, 'ORef', {'Operand' : operand, \
                                          'X' : str(x),
                                          'Y' : str(y),
                                          'HideDesc' : 'false'})
        return new
        
class FBD_TextBox(FBD_Object):
    """Base class for a single Textbox""" 
    text = ElementDescription([], 'Text')
    width = AttributeDescriptor('Width', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)

    @classmethod
    def create(cls, parent, text, x=0, y = 0, width=0):
        new = FBD_Object.create(parent, 'TextBox', {'Width' : str(width),
                                                    'X' : str(x),
                                                    'Y' : str(y)})
        
        """Create Text Element and add CDATA rung data to it"""
        cdataText = parent.doc.createCDATASection(text)
        text_element = parent._create_append_element(new.element, 'Text') 
        text_element.appendChild(cdataText)
        return new
        
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
        
    @classmethod
    def create(cls, parent, fromID, toID):
        wire_length = len(parent.wires)
        element = parent._create_append_element(parent.element, \
                                             'Wire', \
                                             {'FromID' : fromID.ID,
                                              'ToID' : toID.ID})
        new = Wire(element)
        parent.wires.append(str(wire_length), new.element)        
        return new
    