"""
Top-level module defining the Project class through which all L5X access
is performed.

The general approach of this package is to provide access to L5X data
through descriptor objects organized under a Project instance in a structure
similar to RSLogix. These descriptor objects modify XML elements through
the __set__() method or return appropriately converted data from the
__get__() method. In this way the application can process L5X projects
without worrying about low-level XML handling.
"""

from .dom import (ElementAccess, ElementDict, AttributeDescriptor, ElementDescription, ChildElements)
from .module import (Module, SafetyNetworkNumber, CatalogNumber)
from .tag import Scope
from .program import ProgramScope
import xml.dom.minidom
import xml.parsers.expat


class InvalidFile(Exception):
    """Raised if the given .L5X file was not a proper L5X export."""
    pass


class Project(ElementAccess):
    """Top-level container for an entire Logix project."""
    def __init__(self, filename):
        try:
            doc = xml.dom.minidom.parse(filename)
        except xml.parsers.expat.ExpatError as e:
            msg = xml.parsers.expat.ErrorString(e.code)
            raise InvalidFile("XML parsing error: {0}".format(msg))

        if doc.documentElement.tagName != 'RSLogix5000Content':
            raise InvalidFile('Not an L5X file.')

        ElementAccess.__init__(self, doc.documentElement)

        ctl_element = self.get_child_element('Controller')
        self.controller = Controller(ctl_element)
        
        progs = self.controller.get_child_element('Programs')
        self.programs = ElementDict(progs, 'Name', Program)
      
        mods = self.controller.get_child_element('Modules')
        self.modules = ElementDict(mods, 'Name', Module)

    def write(self, filename):
        """Outputs the document to a new file."""
        f = open(filename, 'w')
        self.doc.writexml(f, encoding='UTF-8')
        f.close()


def append_child_element(name, parent):
    """Creates and appends a new child XML element."""
    doc = get_doc(parent)
    new = doc.createElement(name)
    parent.appendChild(new)
    return new


class ControllerSafetyNetworkNumber(SafetyNetworkNumber):
    """Descriptor class for accessing a controller's safety network number.

    This class handles the fact that the controller's safety network number
    is stored as an attribute of the controller's module element rather than
    the top-level controller element. Some additional work is needed to
    direct the superclass's interface to the correct element.
    """
    def __get__(self, instance, owner=None):
        mod = self.get_ctl_module(instance)
        return super(ControllerSafetyNetworkNumber, self).__get__(mod)

    def __set__(self, instance, value):
        mod = self.get_ctl_module(instance)
        super(ControllerSafetyNetworkNumber, self).__set__(mod, value)

    def get_ctl_module(self, instance):
        """Generates an object to access the controller module element.

        While the module's name varies, the controller module is always
        the first child within the Modules element.
        """
        modules = ElementAccess(instance.get_child_element('Modules'))
        return ElementAccess(modules.child_elements[0])

class ProcessorType(AttributeDescriptor):
    """Descriptor class for accessing a controller's processor's type.

    This class handles the fact that the controller's type is stored in two 
    places. With the Controller Element as wells as within the module named local
    The set method gets overloaded so that it writes to the module as well.
    """     
    child_elements = ChildElements()  
        
    def __init__(self):
        """Executes superclass's initializer with attribute name."""
        super(ProcessorType, self).__init__('ProcessorType')
  
    def __set__(self, instance, value):        
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:
            instance.element.setAttribute(self.name, new_value)        
            modules = instance.get_child_element('Modules')            
            modules.getElementsByTagName('Module')[0].setAttribute('CatalogNumber', new_value)
        else:
            raise AttributeError('Cannot remove ProcessorType attribute')  
   
class MajorRev(AttributeDescriptor):
    """Descriptor class for accessing a controller's major revision.

    This class handles the fact that the controller's type is stored in two 
    places. With the Controller Element as wells as within the module named local
    The set method gets overloaded so that it writes to the module as well.
    """     
    child_elements = ChildElements()  
        
    def __init__(self):
        """Executes superclass's initializer with attribute name."""
        super(MajorRev, self).__init__('MajorRev')
  
    def __set__(self, instance, value):        
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:
            instance.element.setAttribute(self.name, new_value)        
            modules = instance.get_child_element('Modules')            
            modules.getElementsByTagName('Module')[0].setAttribute('Major', new_value)
        else:
            raise AttributeError('Cannot remove MajorRev attribute')      

class MinorRev(AttributeDescriptor):
    """Descriptor class for accessing a controller's minor revision.

    This class handles the fact that the controller's type is stored in two 
    places. With the Controller Element as wells as within the module named local
    The set method gets overloaded so that it writes to the module as well.
    """     
    child_elements = ChildElements()  
        
    def __init__(self):
        """Executes superclass's initializer with attribute name."""
        super(MinorRev, self).__init__('MinorRev')
  
    def __set__(self, instance, value):        
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:
            instance.element.setAttribute(self.name, new_value)        
            modules = instance.get_child_element('Modules')            
            modules.getElementsByTagName('Module')[0].setAttribute('Minor', new_value)
        else:
            raise AttributeError('Cannot remove MinorRev attribute')   

class Controller(Scope):
    """Accessor object for the controller device."""
    description = ElementDescription()
    comm_path = AttributeDescriptor('CommPath')
    use = AttributeDescriptor('Use')
    processor_type = ProcessorType()    
    major_revision = MajorRev()
    minor_revision = MinorRev()
    time_slice = AttributeDescriptor('TimeSlice')
    share_unused_time_slice = AttributeDescriptor('ShareUnusedTimeSlice')
    project_creation_date = AttributeDescriptor('ProjectCreationDate')
    last_modified_date = AttributeDescriptor('LastModifiedDate')
    sfc_execution_control = AttributeDescriptor('SFCExecutionControl')
    sfc_restart_position = AttributeDescriptor('SFCRestartPosition')
    sfc_last_scan = AttributeDescriptor('SFCLastScan')
    project_sn = AttributeDescriptor('ProjectSN')
    match_project_to_controller = AttributeDescriptor('MatchProjectToController')
    can_use_rpi_from_producer = AttributeDescriptor('CanUseRPIFromProducer')
    inhibit_automatic_firmware_update = AttributeDescriptor('InhibitAutomaticFirmwareUpdate')
    
    
    snn = ControllerSafetyNetworkNumber()
    
class Program(ProgramScope):
    """Accessor object for a program."""
