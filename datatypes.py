from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement)

class DataType(ElementAccess):
    """Base Data Type container 
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    :var members: :class:`.dom.ElementDict` Dictionary for all datatype members. Accessed by index because order of members matters
    """
    description = ElementDescription()

    def __init__(self, element):
        ElementAccess.__init__(self, element)

        _members = self.get_child_element('Members')
        self.members = ElementDict(_members, types=DataTypeMember)

class DataTypeMember(ElementAccess):
    """Data type members

    :param element: XML element to be used.
    :var name: :class:`.dom.AttributeDescriptor` Name of member
    :var data_type: :class:`.dom.AttributeDescriptor` Data type
    :var dimension: :class:`.dom.AttributeDescriptor` Dimension of array (optional)
    :var radix: :class:`.dom.AttributeDescriptor` Radix
    :var hidden: :class:`.dom.AttributeDescriptor` Hidden member (used mostly for Bit members) (see  1756-RM084V-EN-P Chapter 3)
    :var target: :class:`.dom.AttributeDescriptor` Target member for bit members (see  1756-RM084V-EN-P Chapter 3)
    :var external_access: :class:`.dom.AttributeDescriptor` ExternalAccess
    """

    name = AttributeDescriptor('Name')
    data_type = AttributeDescriptor('DataType')
    dimension = AttributeDescriptor('Dimension')
    radix = AttributeDescriptor('Radix')
    hidden = AttributeDescriptor('Hidden')
    target = AttributeDescriptor('Target')
    external_access = AttributeDescriptor('ExternalAccess')

    def __init__(self, element):
        ElementAccess.__init__(self, element)