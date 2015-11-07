from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement)

class DataType(ElementAccess):
    """Base Data Type container 
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Routine description
    """
    description = ElementDescription()

    def __init__(self, element):
        ElementAccess.__init__(self, element)  
        