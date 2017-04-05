"""
Objects implementing program access.
"""

from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement, ChildElements, ElementDictNames)
from .tag import Tag
from .net_object import *
from .errors import *
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
    test_edits = AttributeDescriptor('TestEdits', False)
    main_routine_name = AttributeDescriptor('MainRoutineName', False)
    disabled = AttributeDescriptor('Disabled', False)

    def __init__(self, element):
        ElementAccess.__init__(self, element)

        tag_element = self.get_child_element('Tags')
        self.tags = ElementDict(tag_element, key_attr='Name', types=Tag)

        routine_element = self.get_child_element('Routines')
        self.routines = ElementDict(routine_element, \
                                    key_attr='Name', \
                                    types={'RLL' : RLLRoutine, \
                                    'FBD' : FBDRoutine, \
                                    'SFC' : SFCRoutine, \
                                    'ST' :  STRoutine,} \
                                    ,\
                                    type_attr="Type")
    @classmethod
    def create(cls, prj, name):
        programs = prj.controller.element.getElementsByTagName('Programs')[0]
        element = prj._create_append_element(programs, \
                                             'Program', \
                                             {'Disabled' : 'false',
                                             'MainRoutineName' : 'MainRoutine',
                                             'Name' : name,
                                             'TestEdits' : 'false'})
        prj._create_append_element(element, 'Tags')
        prj._create_append_element(element, 'Routines')
        program = Program(element)

        routine = RLLRoutine.create(program, 'MainRoutine')
        program.routines.append('MainRoutine', routine)

        return program



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
        return str(value).split(None, 2)[0]

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
    """Base Routine container

    :param element: XML element to be used.
    :var description: :class:`.dom.ElementDescription` Routine description
    :var type: :class:`.dom.AttributeDescriptor` Type of routine, *RLL*, *FBD*, *SFC* or *ST*
    """
    description = ElementDescription()
    type = AttributeDescriptor('Type', False)
    def __init__(self, element):
        ElementAccess.__init__(self, element)


class RLLRoutine(Routine):
    """Ladder Routine Container

    Routines can be one of four types Ladder, Function Block,
    Sequential Function Chart and Structured Text. Each type of routine has
    its own structure.

    :param element: XML element to be used.
    :var rungs: :class:`Rung` Dictionary containing all the rungs. Only available if type is *RLL*"""
    def __init__(self, element):
        Routine.__init__(self, element)
        _rung_element = self.get_child_element('RLLContent')
        self.rungs = ElementDict(_rung_element, key_attr='Number', types=Rung)

    @classmethod
    def create(cls, program, name):
        routines = program.element.getElementsByTagName('Routines')[0]

        element = program._create_append_element(routines, \
                                             'Routine', {'Name' : name,
                                                  'Type' : 'RLL'})
        program._create_append_element(element, 'RLLContent')

        routine = RLLRoutine(element)
        program.routines.append(name, routine.element)
        return routine

class FBDRoutine(Routine):
    """Function Block Routine Container

    Routines can be one of four types Ladder, Function Block,
    Sequential Function Chart and Structured Text. Each type of routine has
    its own structure.

    :param element: XML element to be used.
    :var sheet_size: :class:`.SheetSize` Sheets are sized using standard page sizes *Letter*, *Legal*, *Tabloid*, *A*, *B*, *C*, *D*, *E*, *A4*, *A3*, *A2*, *A1*, *A0*
    :var sheet_orientation: :class:`.dom.AttributeDescriptor` Orientation of sheet. e.g. *Landscape* or *Portrait*
    :var sheets: :class:`Sheet` Dictionary containing all the sheets. Only available if type is *FBD*"""
    sheet_size = SheetSize('FBDContent')
    sheet_orientation = AttributeDescriptor('SheetOrientation', False, 'FBDContent')

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        _fbd_content = self.get_child_element('FBDContent')
        self.sheets = ElementDict(_fbd_content, key_attr='Number', types=Sheet)

    @classmethod
    def create(cls, program, name):
        routines = program.element.getElementsByTagName('Routines')[0]
        element = program._create_append_element(routines, \
                                             'Routine', {'Name' : name,
                                                  'Type' : 'FBD'})
        program._create_append_element(element, 'FBDContent', {'SheetSize' : 'Letter - 8.5 x 11 in',
                                                  'SheetOrientation' : 'Landscape'})

        routine = FBDRoutine(element)
        program.routines.append(name, routine.element)
        return routine

class SFCRoutine(Routine):
    """Sequential Function Chart Routine Container

    Routines can be one of four types Ladder, Function Block,
    Sequential Function Chart and Structured Text. Each type of routine has
    its own structure.

    :param element: XML element to be used.
    :var sheet_size: :class:`.SheetSize` Sheets are sized using standard page sizes *Letter*, *Legal*, *Tabloid*, *A*, *B*, *C*, *D*, *E*, *A4*, *A3*, *A2*, *A1*, *A0*
    :var sheet_orientation: :class:`.dom.AttributeDescriptor` Orientation of sheet. e.g. *Landscape* or *Portrait*
    """
    sheet_size = SheetSize('SFCContent')
    sheet_orientation = AttributeDescriptor('SheetOrientation', False, 'SFCContent')

    def __init__(self, element):
        ElementAccess.__init__(self, element)

    @classmethod
    def create(cls, program, name):
        routines = program.element.getElementsByTagName('Routines')[0]
        element = program._create_append_element(routines, \
                                             'Routine', {'Name' : name,
                                                  'Type' : 'SFC'})
        program._create_append_element(element, 'SFCContent', {'SheetSize' : 'A4 - 210 x 297 mm',
                                                  'SheetOrientation' : 'Landscape'})

        routine = SFCRoutine(element)
        program.routines.append(name, routine.element)
        return routine

class STRoutine(Routine):
    """Structured Text Routine Container

    Routines can be one of four types Ladder, Function Block,
    Sequential Function Chart and Structured Text. Each type of routine has
    its own structure.

    :param element: XML element to be used."""
    def __init__(self, element):
        ElementAccess.__init__(self, element)
        _line_element = self.get_child_element('STContent')
        self.lines = ElementDict(_line_element, key_attr='Number', types=Line)

    @classmethod
    def create(cls, program, name):
        routines = program.element.getElementsByTagName('Routines')[0]
        element = program._create_append_element(routines, \
                                             'Routine', {'Name' : name,
                                                  'Type' : 'ST'})
        program._create_append_element(element, 'STContent')

        routine = STRoutine(element)
        program.routines.append(name, routine.element)
        return routine

class Rung(ElementAccess):
    """A single rung within a Ladder routine.

    Rungs are stored using the raw data from the l5x file

    :param element: XML element to be used.
    :var description: :class:`.dom.ElementDescription` Rung description
    :var number: :class:`.dom.AttributeDescriptor` Rung description
    :var type: :class:`.dom.ElementDescription` Type of rung. Not sure but should indicate if a test/edit has been applied to the rung.
    :var text: Contains the raw l5x text for the rung.
    :var comment: Contains the text for the rung's comment.    """
    description = ElementDescription()
    number = AttributeDescriptor('Number', False)
    type = AttributeDescriptor('Type', False)

    def __init__(self, element):
        ElementAccess.__init__(self, element)

    @property
    def text(self):
        """
        The text of the rung

        :getter: Returns the text of the rung, or empty string if not found
        :setter: Sets the rung text
        :type: string
        """
        try:
            return str(CDATAElement(self.get_child_element('Text')))
        except KeyError:
            return ""

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Rung text must be string")
        if not value.endswith(";"):
            raise ValueError("Ladder Logic rungs must end with a semicolon")
        CDATAElement(self.get_child_element('Text')).set(value)

    @property
    def comment(self):
        """
        The text of the comment for the rung

        :getter: Returns the text of the comment, or empty string if not found
        :setter: Sets the rung comment
        :type: string
        """
        try:
            return str(CDATAElement(self.get_child_element('Comment')))
        except KeyError:
            return ""

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise TypeError("Rung comment must be string")
        try:
            CDATAElement(self.get_child_element('Comment')).set(value)
        except KeyError:
            element = self.create_element('Comment', {})
            self.element.insertBefore(element, self.element.firstChild)
            node = self.doc.createCDATASection('')
            element.appendChild(node)
            CDATAElement(self.get_child_element('Comment')).set(value)

    @classmethod
    def create(cls, routine, text, number=None):
        """Confirms the rung number isn't out of range"""
        if number is None:
            number = len(routine.rungs)
        else:
            lastnumber = routine.getLastRungNumber()
            if not (number >= 0 and number < lastnumber):
                raise RungNumberOutOfRangeError()
        if not text.endswith(";"):
            raise ValueError("Ladder Logic rungs must end with a semicolon")
        """Selects the RLLContent element to add the rung to"""
        rllcontent = routine.element.getElementsByTagName('RLLContent')[0]
        element = routine._create_append_element(rllcontent, \
                                             'Rung', {'Number' : str(number),
                                                  'Type' : 'N'})
        """Create Text Element and add CDATA rung data to it"""
        cdataText =routine.doc.createCDATASection(text)
        text_element = routine._create_append_element(element, 'Text')
        text_element.appendChild(cdataText)

        rung = Rung(element)
        routine.rungs.append(str(number), rung.element)
        return rung

class Line(ElementAccess):
    """A single line within a structured text routine.

    Lines are stored as raw strings from the L5X file

    :param element: XML element to be used.
    :var description: :class:`.dom.ElementDescription` Rung description
    :var number: :class:`.dom.AttributeDescriptor` Rung description
    :var text: Contains the raw l5x text for the rung.    """
    description = ElementDescription()
    number = AttributeDescriptor('Number', True)

    def __init__(self, element):
        ElementAccess.__init__(self, element)
        self.text = str(CDATAElement(self.get_child_element('Text')))

class Sheet(ElementAccess):
    """A single sheet to be contained within a function block routine.

    Sheets contain blocks and wires. The type is used to determine the
    type of block. Wires connect two pins together

    :param element: XML element to be used.
    :var description: :class:`.dom.ElementDescription` Rung description
    :var blocks: :class:`.dom.ElementDict` Dictionary used to store all logic blocks
    :var wire: :class:`.dom.ElementDict` Dictionary used to store all interconnecting wires
    """
    description = ElementDescription()

    def __init__(self, element):
        ElementAccess.__init__(self, element)

        self.blocks = ElementDict(element, \
                            key_attr='ID', \
                            types={'IRef' : FBD_IRef, \
                            'ORef' : FBD_ORef, \
                            'TextBox' : FBD_TextBox,
                            'DefaultType' : FBD_Default},
                            use_tagname= True, \
                            attr_filter = 'ID')

        self.wires = ElementDict(self.element, \
                                types=Wire, \
                                tag_filter="Wire")

    @classmethod
    def create(cls, routine, number=None):
        """Confirms the sheet number isn't out of range"""
        if number is None:
            number = len(routine.sheets) + 1
        else:
            if not (number >= 0 and number < len(routine.sheets)):
                raise SheetNumberOutOfRangeError()
        """Selects the FBDContent element to add the sheet to"""
        content = routine.element.getElementsByTagName('FBDContent')[0]
        element = routine._create_append_element(content, \
                                             'Sheet', {'Number' : str(number)})
        sheet = Sheet(element)
        routine.sheets.append(str(number), sheet.element)
        return sheet
