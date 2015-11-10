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
from .program import Program
from .errors import InvalidFile
from .datatypes import DataType
from .addoninstructions import AddOns
import xml.dom.minidom
import xml.parsers.expat

class Project(ElementAccess):
    """Top-level container for an entire Logix project.
        
    :param filename: File to be parsed in the l5x structure 
    :var schema_revision: :class:`.dom.AttributeDescriptor` The L5X schema revision that was used to write the file.
    :var target_name: :class:`.dom.AttributeDescriptor` The name of the controller from which the L5x was created, if *target_type* = *Controller*.
    :var target_type: :class:`.dom.AttributeDescriptor` The type of export this file is. *Controller*
    :var contains_context: :class:`.dom.AttributeDescriptor` 
    :var owner: :class:`.dom.AttributeDescriptor` The author/owner of the program.
    :var export_options: :class:`.dom.AttributeDescriptor` Options for what to include in the export. Options available are:- Decorated Data, ForceProtectedEncoding, AllProjDocTrans
    :var programs: :class:`.dom.ElementDict` Dictionary for all programs and their routines
    :var controller: :class:`Controller` Container for PLC specific information such as type, serial number, etc..
    :var modules: :class:`.dom.ElementDict` Dictionary for Hardware modules and layout"""
    schema_revision = AttributeDescriptor('SchemaRevision')
    target_type = AttributeDescriptor('TargetType')
    contains_context = AttributeDescriptor('ContainsContext')
    owner = AttributeDescriptor('Owner')
    export_options = AttributeDescriptor('ExportOptions')  
   
    def __init__(self, filename=None):
        if filename is not None:
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
        else:
            _doc = xml.dom.minidom.parseString('<RSLogix5000Content \
                          SchemaRevision="1.0" \
                          SoftwareRevision = "" \
                          TargetName = "" \
                          TargetType = "Controller" \
                          ContainsContext = "false" \
                          Owner = "Default" \
                          ExportDate = "Mon Nov 02 04:15:51 2015" \
                          ExportOptions = "DecoratedData ForceProtectedEncoding AllProjDocTrans"></RSLogix5000Content>')
            ElementAccess.__init__(self, _doc.documentElement)

            Controller.create(self)
            
        _datatypes = self.controller.get_child_element('DataTypes')
        self.datatypes = ElementDict(_datatypes, key_attr='Name', types=DataType) 
        
        _addoninstructions = self.controller.get_child_element('AddOnInstructionDefinitions')
        self.addons = ElementDict(_addoninstructions, key_attr='Name', types=AddOns) 
        
        _programs = self.controller.get_child_element('Programs')
        self.programs = ElementDict(_programs, key_attr='Name', types=Program) 
      
        _modules = self.controller.get_child_element('Modules')
        self.modules = ElementDict(_modules, key_attr='Name', types=Module)
            
        if filename is None:
            Module.createController(self)
            program = Program.create(self, 'MainProgram')
            self.programs.append('MainProgram', program.element)
              
    def write(self, filename):
        """Writes the l5x structure to a file
        
        :param filename: path to output file"""
        file = open(filename, 'w')
        self.doc.writexml(file, addindent="", newl="\n", encoding='UTF-8')
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
   
class TargetName(AttributeDescriptor):
    """Descriptor class for accessing a controller name."""
             
    def __init__(self):
        """Helps make it easier when the revision needs to be changed
        by modifying the underlying XML elements. It is stored in two places project.controller
        as well as the XML element for project.module['Local']"""  
        self._child_elements = ChildElements() 
        """Executes superclass's initializer with attribute name."""
        super(TargetName, self).__init__('Name')
  
    def __set__(self, instance, value):        
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:
            instance.element.setAttribute(self.name, new_value) 
            #Write the major revision to the controller specified in the hardware list   
            instance.element.parentNode.setAttribute('TargetName', new_value)
        else:
            raise AttributeError('Cannot remove TargetName attribute')      


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
            #Write the major revision to the controller specified in the hardware list       
            modules = instance.get_child_element('Modules')            
            modules.getElementsByTagName('Module')[0].setAttribute('Major', new_value)
            #Write the major revision to the RSLogix5000 element.
            _rslogix = instance.element.parentNode.getAttribute("SoftwareRevision")
            instance.element.parentNode.setAttribute("SoftwareRevision", value + "." + _rslogix[3:])
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
            #Write the minor revision to the controller specified in the hardware list           
            modules = instance.get_child_element('Modules')            
            modules.getElementsByTagName('Module')[0].setAttribute('Minor', new_value)
            #Write the minor revision to the RSLogix5000 element.
            _rslogix = instance.element.parentNode.getAttribute("SoftwareRevision")
            instance.element.parentNode.setAttribute("SoftwareRevision", _rslogix[:2] + "." + value)
        else:
            raise AttributeError('Cannot remove MinorRev attribute')   
        
class Slot(AttributeDescriptor):
    """Descriptor class for accessing a slot number."""
   
    def __init__(self):
        """Helps make it easier when the slot needs to be changed
        by modifying the underlying XML elements. It is stored in two places project.controller
        as well as the XML element for project.module['Local'].Ports.Port"""  
        self._child_elements = ChildElements() 
        """Executes superclass's initializer with attribute name."""
        super(Slot, self).__init__('Slot')
  
    def __get__(self, instance, value):   
        raw = None                
        modules = instance.get_child_element('Modules')            
        module = modules.getElementsByTagName('Module')[0]
        ports = module.getElementsByTagName('Ports')[0]
        if (ports.getElementsByTagName('Port')[0].hasAttribute(self.name)):
                raw = ports.getElementsByTagName('Port')[0].getAttribute('Address') 
        if raw is not None:      
            return self.from_xml(raw)
        return None 
   
    def __set__(self, instance, value):        
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:
            #Write the slot number to the controller specified in the hardware list           
            modules = instance.get_child_element('Modules')            
            module = modules.getElementsByTagName('Module')[0]
            ports = module.getElementsByTagName('Ports')[0]
            ports.getElementsByTagName('Port')[0].setAttribute('Address', new_value)
        else:
            raise AttributeError('Cannot remove MinorRev attribute')  

class Controller(Scope):
    """Container class to store controller specific settings
    
    :param element: XML element to be used to populate structure 
    :var programs: :class:`.dom.ElementDict`  Dictionary containing all programs
    :var description: :class:`.dom.ElementDescription` Controller description
    :var comm_path: :class:`.dom.AttributeDescriptor` Communication path configured using <RSLinx Node>\<IP Address>\Slot Number. This is the node from the computer to the processor
    :var use: :class:`.dom.AttributeDescriptor` This is associated with the context to be used when import the l5x into RSLogix 5000
    :var processor_type: :class:`ProcessorType` The processor type is identified using a part number with the format:-<controller family>-<module type>. e.g. 1756-L75
    :var major_revision: :class:`MajorRev` Major Revision number of processor firmware
    :var minor_revision: :class:`MinorRev` Minor revision number of processor
    :var time_slice: :class:`.dom.AttributeDescriptor` The percentage of the processors time that should be allocated for communications tasks.
    :var share_unused_time_slice: :class:`.dom.AttributeDescriptor` Selection of whether or not to use the unused time for the continous task or not
    :var project_creation_date: :class:`.dom.AttributeDescriptor` Date project was first created. e.g. "Mon Nov 02 04:15:51 2015"
    :var last_modified_date: :class:`.dom.AttributeDescriptor` Date project was last modified. e.g. "Mon Nov 02 04:15:51 2015"
    :var sfc_execution_control: :class:`.dom.AttributeDescriptor` Unsure. e.g. "CurrentActive"
    :var sfc_restart_position: :class:`.dom.AttributeDescriptor`Unsure. e.g. "MostRecent"
    :var sfc_last_scan: :class:.dom.`AttributeDescriptor` Unsure. e.g. "MostRecent"
    :var project_sn: :class:`.dom.AttributeDescriptor` Serial number of the processor that the project is tied to. e.g. 16#0000_0000
    :var match_project_to_controller: :class:`.dom.AttributeDescriptor`  Boolean to indicate the project can only be downloaded to the serial number specified with `match_project_to_controller`
    :var can_use_rpi_from_producer: :class:`.dom.AttributeDescriptor` Allow a tag producer to specify the RPI to be used. Normally the consumer specifies this.
    :var inhibit_automatic_firmware_update: :class:`.dom.AttributeDescriptor` Selection to block the update of the processor firmware
    :var snn: :class:`ControllerSafetyNetworkNumber` Safety network number used  in safety controllers.
    :var redundancy_enabled: :class:`.dom.AttributeDescriptor` Enable/Disable the controllers redundancy feature.
    :var redundancy_keep_test_edits_on_switchover: :class:`.dom.AttributeDescriptor` Enable/Disable the mirroring of test/edits between redundant processors.
    :var redundancy_io_memory_pad_percentage: :class:`.dom.AttributeDescriptor` Unknown.
    :var redundancy_datatable_pad_percentage: :class:`.dom.AttributeDescriptor` Unknown.
    """
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
    redundancy_enabled = AttributeDescriptor('Enabled', False, 'RedundancyInfo')
    redundancy_keep_test_edits_on_switchover = AttributeDescriptor('KeepTestEditsOnSwitchOver', False, 'RedundancyInfo')
    redundancy_io_memory_pad_percentage = AttributeDescriptor('IOMemoryPadPercentage', False, 'RedundancyInfo')
    redundancy_datatable_pad_percentage = AttributeDescriptor('DataTablePadPercentage', False, 'RedundancyInfo')
    target_name = TargetName()    
    slot = Slot()

    def __init__(self, element):
        """Executes superclass's initializer with attribute name."""        
        Scope.__init__(self, element)   
        
    @classmethod
    def create(cls, prj):
        element = prj._create_append_element(prj.element, 'Controller', {'Use' : 'Target',\
                                                                  'Name' : '',\
                                                                  'ProcessorType' : '',\
                                                                  'MajorRev' : '',\
                                                                  'MinorRev' : '',\
                                                                  'TimeSlice' : '20',\
                                                                  'ShareUnusedTimeSlice' : '1',\
                                                                  'ProjectCreationDate' : '',\
                                                                  'LastModifiedDate' : '',\
                                                                  'SFCExecutionControl' : 'CurrentActive',\
                                                                  'SFCRestartPosition' : 'MostRecent',\
                                                                  'SFCLastScan' : 'DontScan',\
                                                                  'ProjectSN' : '16#0000_0000',\
                                                                  'MatchProjectToController' : 'false'})            
        prj._create_append_element(element, 'RedundancyInfo', {'Enabled' : 'false', \
                                                               'KeepTestEditsOnSwitchOver' : 'false',
                                                               'IOMemoryPadPercentage' : '90',
                                                               'DataTablePadPercentage' : '50'})
        prj._create_append_element(element, 'Security', {'Code' : '0', \
                                                               'ChangesToDetect' : '16#ffff_ffff_ffff_ffff',
                                                               'IOMemoryPadPercentage' : '90',
                                                               'DataTablePadPercentage' : '50'})
        prj._create_append_element(element, 'SafetyInfo')
        prj._create_append_element(element, 'DataTypes')
        prj._create_append_element(element, 'Modules')
        prj._create_append_element(element, 'AddOnInstructionDefinitions')   
        prj._create_append_element(element, 'Tags')   
        prj.controller = Controller(element)     
        prj._create_append_element(prj.controller.element, 'Programs') 
        

    

