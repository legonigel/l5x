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
from .module import (Module, SafetyNetworkNumber)
from .tag import Scope
from .program import ProgramScope
from .errors import InvalidFile
import xml.dom.minidom
import xml.parsers.expat

class Project(ElementAccess):
    """Top-level container for an entire Logix project.
        
    :param filename: File to be parsed in the l5x structure    
    :var programs: :class:`ElementDict` Dictionary for all programs and their routines
    :var controller: :class`Controller` Container for PLC specific information such as type, serial number, etc..
    :var modules: :class:`ElementDict` Dictionary for Hardware modules and layout"""
    def __init__(self, filename):
        try:
            _doc = xml.dom.minidom.parse(filename)
        except xml.parsers.expat.ExpatError as e:
            _msg = xml.parsers.expat.ErrorString(e.code)
            raise InvalidFile("XML parsing error: {0}".format(_msg))

        if _doc.documentElement.tagName != 'RSLogix5000Content':
            raise InvalidFile('Not an L5X file.')

        ElementAccess.__init__(self, _doc.documentElement)
        
        _controller = self.get_child_element('Controller')        
        self.controller = Controller(_controller)
        
        _programs = self.controller.get_child_element('Programs')
        self.programs = ElementDict(_programs, 'Name', Program) 
      
        _modules = self.controller.get_child_element('Modules')
        self.modules = ElementDict(_modules, 'Name', Module)

    def write(self, filename):
        """Writes the l5x structure to a file
        
        :param filename: path to output file"""
        file = open(filename, 'w')
        self.doc.writexml(file, encoding='UTF-8')
        file.close()


    def append_child_element(self, name, parent):
        """Creates and appends a new child XML element.
                
        :param name: Name of element to be appended
        :param parent: Where new element should be attached"""
        temp_doc = self.get_doc(parent)
        new = temp_doc.createElement(name)
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
    
    The processor type is identified using a part number with the format:-
    \"controller family-module type\". e.g. \"1756-L75\""""
    def __init__(self):
        """ProcessorType is to help make it easier when the processor type needs to be changed
        by modifying the underlying XML elements. It is stored in two places project.controller
        as well as the XML element for project.module['Local']"""
        self._child_elements = ChildElements()  
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

    The revision of the processer's firmware is stored as a major and minor revision
    such as 20.11 or 19.01"""             
    def __init__(self):
        """Helps make it easier when the revision needs to be changed
        by modifying the underlying XML elements. It is stored in two places project.controller
        as well as the XML element for project.module['Local']"""  
        self._child_elements = ChildElements() 
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
    """Descriptor class for accessing a controller's major revision.

    The revision of the processer's firmware is stored as a major and minor revision
    such as 20.11 or 19.01"""         
    def __init__(self):
        """Helps make it easier when the revision needs to be changed
        by modifying the underlying XML elements. It is stored in two places project.controller
        as well as the XML element for project.module['Local']"""  
        self._child_elements = ChildElements() 
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
    """Container class to store controller specific settings
    
    :param element: XML element to be used to populate structure 
    :var programs: :class:`ElementDict`  Dictionary containing all programs
    :var description: :class:`ElementDescription` Controller description
    :var comm_path: :class:`AttributeDescriptor` Communication path configured using <RSLinx Node>\<IP Address>\Slot Number. This is the node from the computer to the processor
    :var use: :class:`AttributeDescriptor` This is associated with the context to be used when import the l5x into RSLogix 5000
    :var processor_type: :class:`ProcessorType` The processor type is identified using a part number with the format:-<controller family>-<module type>. e.g. 1756-L75
    :var major_revision: :class:`MajorRev` Major Revision number of processor firmware
    :var minor_revision: :class:`MinorRev` Minor revision number of processor
    :var time_slice: :class:`AttributeDescriptor` The percentage of the processors time that should be allocated for communications tasks.
    :var share_unused_time_slice: :class:`AttributeDescriptor` Selection of whether or not to use the unused time for the continous task or not
    :var project_creation_date: :class:`AttributeDescriptor`
    :var last_modified_date: :class:`AttributeDescriptor`
    :var sfc_execution_control: :class:`AttributeDescriptor`
    :var sfc_restart_position: :class:`AttributeDescriptor`
    :var sfc_last_scan: :class:`AttributeDescriptor`
    :var project_sn: :class:`AttributeDescriptor`
    :var match_project_to_controller: :class:`AttributeDescriptor`
    :var can_use_rpi_from_producer: :class:`AttributeDescriptor`
    :var inhibit_automatic_firmware_update: :class:`AttributeDescriptor`
    :var snn: :class:`ControllerSafetyNetworkNumber`"""

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

    def __init__(self, element):    
        """Executes superclass's initializer with attribute name."""
        Scope.__init__(self, element)
    
class Program(ProgramScope):
    """Accessor object for a program."""
