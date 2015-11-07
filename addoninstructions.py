from .dom import (ElementAccess, ElementDict, AttributeDescriptor,
                  ElementDescription, CDATAElement)

class AddOns(ElementAccess):
    """Base Add On Instruction Definitions container 
    
    :param element: XML element to be used.    
    :var description: :class:`.dom.ElementDescription` Add On description
    """
    description = ElementDescription()

    def __init__(self, element):
        ElementAccess.__init__(self, element)  

