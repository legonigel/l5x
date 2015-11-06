"""
Objects implementing program access.
"""

from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement, ChildElements, ElementDictNames)
from .tag import Tag
from .net_object import *

import ctypes
import string
import xml.dom

class Program(ElementAccess):
    """Top level container to hold a program in.
    
    Container to hold a group of tags and routines within a specific scope.
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Program description
    :var test_edits: :class:`.dom.AttributeDescriptor` Indication of whether or not any edits or test sections of logic are in place
    :var main_routine_name: :class:`.dom.AttributeDescriptor` Name  of the main routine.This routine is the only routine that is implicitly called within the program.
    :var disabled: :class:`.dom.AttributeDescriptor` Indication of whether or not the program has been disabled.
    :var tags: :class:`.dom.ElementDict` Dictionary for storing program scoped tags
    :var routines: :class:`.dom.ElementDict` Dictionary for routines"""  
    description = ElementDescription()
    test_edits = AttributeDescriptor('TestEdits', True)
    main_routine_name = AttributeDescriptor('MainRoutineName', True)  
    disabled = AttributeDescriptor('Disabled', True)  
        
    def __init__(self, element):
        ElementAccess.__init__(self, element)

        tag_element = self.get_child_element('Tags')
        self.tags = ElementDict(tag_element, 'Name', Tag)
        
        routine_element = self.get_child_element('Routines')
        self.routines = ElementDict(routine_element, \
                                    'Name', \
                                    {'RLL' : RLLRoutine, \
                                    'FBD' : FBDRoutine, \
                                    'SFC' : SFCRoutine, \
                                    'ST' :  STRoutine,} \
                                    ,type_attr="Type")
                   
class SheetSize(AttributeDescriptor):
    """Descriptor class for accessing a routines sheet size.

    The sheet size is stored as a string with size and measurements within the 
    l5x file. e.g. *Letter - 8.5 x 11 in*. This descriptor removes the measurements
    when the object is returned and only returns the size e.g. *A4* or *Legal*
    :var full_size_measurements: the raw l5x string can also be requested if required.
    """         
    def __init__(self, use_element):
        """Helps make it easier as the measurements aren't generally required."""  
        self._child_elements = ChildElements() 
        """Executes superclass's initializer with attribute name."""
        super(SheetSize, self).__init__('SheetSize', False, use_element)
                    
    def from_xml(self, value):
        """Strips the measurements from the size description
        
        :param value: string with the size and measurement of the sheet. e.g. *Letter - 8.5 x 14 in*"""
        return str(value).split(maxsplit=2)[0]

    def to_xml(self, value):
        """Adds the measurement description when writing the l5x file.
        
        :param value: string with the size of the sheet. e.g. *A0* or *Letter*"""
        if (value is not None) and (not isinstance(value, str)):
            raise TypeError('Value must be a string')
        if value == "Letter":
            value = "Letter - 8.5 x 14 in"
        elif value == "Legal":
            value = "Legal - 8.5 x 11 in"
        elif value == "Tabloid":
            value = "Tabloid - 11 x 17 in"
        elif value == "A":
            value = "A - 8.5 x 11 in"
        elif value == "B":
            value = "B - 11 x 17 in"
        elif value == "C":
            value = "C - 17 x 22 in"
        elif value == "D":
            value = "D - 22 x 34 in"
        elif value == "E":
            value = "E - 34 x 44 in"
        elif value == "A4":
            value = "A4 - 210x297 mm"
        elif value == "A3":
            value = "A3 - 297x420 mm"
        elif value == "A2":
            value = "A2 - 420x594 mm"
        elif value == "A1":
            value = "A1 -594x841 mm"
        elif value == "A0":
            value = "A0 - 841x1189 mm" 
        return value

class Routine(ElementAccess):
    pass

class RLLRoutine(Routine):
    """Ladder Routine Container
     
    Routines can be one of four types Ladder, Function Block, 
    Sequential Function Chart and Structured Text. Each type of routine has 
    its own structure.
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    :var type: :class:`.dom.AttributeDescriptor` Type of routine, *RLL*, *FBD*, *SFC* or *ST*
    :var rungs: :class:`Rung` Dictionary containing all the rungs. Only available if type is *RLL*"""
    description = ElementDescription()
    type = AttributeDescriptor('Type', True)    

    def __init__(self, element):
        ElementAccess.__init__(self, element)  
        rung_element = self.get_child_element('RLLContent')
        self.rungs = ElementDict(rung_element, 'Number', Rung)

class FBDRoutine(Routine):
    """Function Block Routine Container
     
    Routines can be one of four types Ladder, Function Block, 
    Sequential Function Chart and Structured Text. Each type of routine has 
    its own structure.
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    :var type: :class:`.dom.AttributeDescriptor` Type of routine, *RLL*, *FBD*, *SFC* or *ST*   
    :var sheet: :class:`Sheet` Dictionary containing all the sheets. Only available if type is *FBD*"""
    description = ElementDescription()
    type = AttributeDescriptor('Type', True)
    sheet_size = SheetSize('FBDContent')    

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        _fbd_content = self.get_child_element('FBDContent')            
        self.sheets = ElementDict(_fbd_content, 'Number', Sheet)

class SFCRoutine(Routine):
    """Ladder Routine Container
     
    Routines can be one of four types Ladder, Function Block, 
    Sequential Function Chart and Structured Text. Each type of routine has 
    its own structure.
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    :var type: :class:`.dom.AttributeDescriptor` Type of routine, *RLL*, *FBD*, *SFC* or *ST*
    :var rungs: :class:`Rung` Dictionary containing all the rungs. Only available if type is *RLL*
    :var sheet: :class:`Sheet` Dictionary containing all the sheets. Only available if type is *FBD*"""
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

class STRoutine(Routine):
    """Ladder Routine Container
     
    Routines can be one of four types Ladder, Function Block, 
    Sequential Function Chart and Structured Text. Each type of routine has 
    its own structure.
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    :var type: :class:`.dom.AttributeDescriptor` Type of routine, *RLL*, *FBD*, *SFC* or *ST*
    :var rungs: :class:`Rung` Dictionary containing all the rungs. Only available if type is *RLL*
    :var sheet: :class:`Sheet` Dictionary containing all the sheets. Only available if type is *FBD*"""
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
    """A single rung within a Ladder routine.
     
    Rungs are stored using the raw data from the l5x file
    
    :param element: XML element to be used.   
    :var description: :class:`.dom.ElementDescription` Rung description 
    :var number: :class:`.dom.AttributeDescriptor` Rung description
    :var type: :class:`.dom.ElementDescription` Type of rung. Not sure but should indicate if a test/edit has been applied to the rung.
    :var text: Contains the raw l5x text for the rung.    """
    description = ElementDescription()
    number = AttributeDescriptor('Number', True)   
    type = AttributeDescriptor('Type', True) 

    def __init__(self, element):
        ElementAccess.__init__(self, element)        
        self.text = str(CDATAElement(self.get_child_element('Text')))
        


class Sheet(ElementAccess):
    """A single sheet to be contained within a function block routine.
     
    Sheets contain blocks and wires. The type is used to determine the 
    type of block. Wires connect two pins together
    
    :param element: XML element to be used. 
    :var description: :class:`.dom.ElementDescription` Rung description    
    :var sheet_size: :class:`.SheetSize` Sheets are sized using standard page sizes *Letter*, *Legal*, *Tabloid*, *A*, *B*, *C*, *D*, *E*, *A4*, *A3*, *A2*, *A1*, *A0*"""
    description = ElementDescription() 
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
     
