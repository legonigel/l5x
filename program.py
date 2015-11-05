"""
Objects implementing program access.
"""

from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement)
import ctypes
from .tag import Tag
from .net_object import *

class ProgramScope(ElementAccess):
    description = ElementDescription()
    test_edits = AttributeDescriptor('TestEdits', True)
    main_routine_name = AttributeDescriptor('MainRoutineName', True)  
    disabled = AttributeDescriptor('Disabled', True)  
    
    """Container to hold a group of tags and routines within a specific scope."""
    def __init__(self, element):
        ElementAccess.__init__(self, element)

        tag_element = self.get_child_element('Tags')
        self.tags = ElementDict(tag_element, 'Name', Tag)
        
        routine_element = self.get_child_element('Routines')
        self.routines = ElementDict(routine_element, 'Name', Routine)

class Routine(ElementAccess):
    """Base class for a single routine."""
    description = ElementDescription()
    type = AttributeDescriptor('Type', True)    

    def __init__(self, element):
        ElementAccess.__init__(self, element)        
        if self.type == "RLL":
            rung_element = self.get_child_element('RLLContent')
            self.rungs = ElementDict(rung_element, 'Number', Rung)
        elif self.type == "FBD":            
            sheet_element = self.get_child_element('FBDContent')            
            self.sheets = ElementDict(sheet_element, 'Number', Sheet)

class Rung(ElementAccess):
    """Base class for a single rung."""
    description = ElementDescription()
    number = AttributeDescriptor('Number', True)   
    type = AttributeDescriptor('Type', True) 

    def __init__(self, element):
        ElementAccess.__init__(self, element)        
        self.text = str(CDATAElement(self.get_child_element('Text')))
        
class Sheet(ElementAccess):
    """Base class for a single sheet."""
    description = ElementDescription()
    sheet_size = AttributeDescriptor('SheetSize', True)   
    sheet_orientation = AttributeDescriptor('SheetOrientation', True)  

    def __init__(self, element):
        ElementAccess.__init__(self, element)        
      
        self.iref = ElementDict(self.element, \
                                'ID', \
                                IRef, \
                                use_filter=True, \
                                filter="IRef")
        self.oref = ElementDict(self.element, \
                                'ID', \
                                ORef, \
                                use_filter=True, \
                                filter="ORef")
        self.textbox = ElementDict(self.element, \
                                   'ID', \
                                   TextBox, \
                                   use_filter=True, \
                                   filter="TextBox")
        self.wire = ElementDict(self.element, \
                                '', \
                                Wire, \
                                seq_key=True, \
                                use_filter=True, \
                                filter="Wire")
     

