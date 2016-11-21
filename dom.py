"""
Internal XML DOM helper inteface objects.
"""

import xml.dom


class ChildElements(object):
    """Descriptor class to acquire a list of child elements."""
    def __get__(self, accessor, owner=None):
        nodes = accessor.element.childNodes
        return [n for n in nodes if n.nodeType == n.ELEMENT_NODE]

        
class ElementAccess(object):
    """Generic base interface for accessing an XML element."""
    child_elements = ChildElements()

    def __init__(self, element):
        self.element = element
        self.get_doc()

    def get_doc(self):
        """Extracts a reference to the top-level XML document."""
        node = self.element
        while node.parentNode != None:            
            node = node.parentNode
        self.doc = node

    def get_child_element(self, name):
        """Finds a child element with a specific tag name."""
        for e in self.child_elements:
            if (e.tagName == name):
                return e

        raise KeyError()

    def create_element(self, name, attributes={}):
        """Wrapper to create a new element with a set of attributes."""
        new = self.doc.createElement(name)
        for attr in attributes.keys():
            new.setAttribute(attr, attributes[attr])
        return new

    def _create_append_element(self, parent, name, attributes={}):  
        new = self.create_element(name, attributes) 
        parent.appendChild(new)        
        return new

    def append_child(self, node):
        """Appends a node to the element's set of children."""
        self.element.appendChild(node)


class CDATAElement(ElementAccess):
    """
    This class manages access to CDATA content contained within a dedicated
    XML element. Examples of uses are tag descriptions and comments.
    """
    def __init__(self, element=None, parent=None, name=None, attributes={}):
        """
        When instantiated this can access an existing element or create
        a new one.
        """
        if element is not None:
            ElementAccess.__init__(self, element)
            self.get_existing()
        else:
            element = parent.create_element(name, attributes)
            ElementAccess.__init__(self, element)

            # Add the child CDATA section.
            self.node = parent.doc.createCDATASection('')
            self.append_child(self.node)

    def get_existing(self):
        """Locates a CDATA node within an existing element."""
        for child in self.element.childNodes:
            if child.nodeType == child.CDATA_SECTION_NODE:
                self.node = child

        # Verify a CDATA node was found.
        try:
            s = str(self)
        except AttributeError:
            raise AttributeError('No CDATA node found')

    def __str__(self):
        """Returns the current string content."""
        return self.node.data

    def set(self, s):
        """Sets the CDATA section content."""
        self.node.data = s


class ElementDescription(object):
    """Descriptor class for accessing a top-level Description element.

    Description elements contain a CDATA comment for some type of
    container element, such as a Tag or Module.
     
    :param follow: A List of elements which must come before the description element. This is use when creating a description to confirm it is place in the correct order.
    :param element: XML element associated with this description
    :param element: If the description isn't contained in an element called Description then use a this element name
    """
    def __init__(self, follow=[], use_element='Description'):
        """Store a list of elements which must preceed the description."""
        self.follow = follow   
        self.use_element = use_element

    def __get__(self, instance, owner=None):
        """Returns the current description string."""
        try:
            element = instance.get_child_element(self.use_element)
        except KeyError:
            return None
        cdata = CDATAElement(element)
        return str(cdata)

    def __set__(self, instance, value):
        """Modifies the description text."""
        # Set a new description if given a string value, creating a new
        # element if necessary.
        if isinstance(value, str):
            try:
                element = instance.get_child_element(self.use_element)
            except KeyError:
                cdata = self.create(instance)
            else:
                cdata = CDATAElement(element)

            cdata.set(value)

        # A value of None removes any existing description.
        elif value is None:
            try:
                element = instance.get_child_element(self.use_element)
            except KeyError:
                pass
            else:
                instance.element.removeChild(element)
                element.unlink()

        else:
            raise TypeError('Description must be a string or None')

    def create(self, instance):
        """Creates a new Description element."""
        new = CDATAElement(parent=instance, name=self.use_element)

        # Search for any elements listed in the follow attribute.
        follow = None
        for e in instance.child_elements:
            if e.tagName in self.follow:
                follow = e

        # Create as first child if no elements to follow were found.
        if follow is None:
            instance.element.insertBefore(new.element,
                                          instance.element.firstChild)

        # If any follow elements exist, insert the new description
        # element after the last one found. DOM node operations do not
        # provide an append-after method so an insert-remove-insert
        # procedure is used.
        #Possibly is causing white space after CDATA element.
        else:
            instance.element.insertBefore(new.element, follow)
            instance.element.removeChild(follow)
            instance.element.insertBefore(follow, new.element)

        return new


class AttributeDescriptor(object):
    """Generic descriptor class for accessing an XML element's attribute.
    
    This relies on the XML element being associated with the element attribute
    of the instance. The attribute can be read from this element. If however 
    the attribute belongs to a child of the instances element. Then the element 
    to use can be defined using the use_element parameter.
        
    :param name: The name of the XML attribute to use
    :param read_only: If enabled disables the ability to write to this attribute.
    :param use_element: If a child XML element contains the attribute to return then use this element instead"""
    def __init__(self, name, read_only=False, use_element=None):
        self.name = name
        self.read_only = read_only
        self.use_element = use_element

    def __get__(self, instance, owner=None): 
        raw = None
        #If the current element should be used to look for the attribute
        if self.use_element is None:            
            if (instance.element.hasAttribute(self.name)):
                raw = instance.element.getAttribute(self.name) 
        else: # If a child element named *use_elment* should be used.
            _use_element = instance.get_child_element(self.use_element)
            if (_use_element.hasAttribute(self.name)):
                raw = _use_element.getAttribute(self.name)  
        if raw is not None:      
            return self.from_xml(raw)
        return None               

    def __set__(self, instance, value):
        if self.read_only is True:
            raise AttributeError('Attribute is read-only')
        new_value = self.to_xml(value)
        if new_value is not None:            
            if self.use_element is None:  # is the current element should be used              
                instance.element.setAttribute(self.name, new_value)   
            else: #If a child element should be used
                _use_element = instance.get_child_element(self.use_element)
                _use_element.setAttribute(self.name, new_value)
 
        # Delete the attribute if value is None, ignoring the case if the
        # attribute didn't exist to begin with.
        else:
            try:
                if self.use_element is None:
                    instance.element.removeAttribute(self.name)
                else:
                    _use_element = instance.get_child_element(self.use_element)
                    _use_element.removeAttribute(self.name)
            except xml.dom.NotFoundErr:
                pass


    def from_xml(self, value):
        """Default converter for reading attribute string.

        Can be overridden in subclasses to provide custom conversion.
        """
        return str(value)

    def to_xml(self, value):
        """Default converter for writing attribute string.

        Subclasses may implement custom conversions from user values
        by overriding this method. Must return a string or None.
        """
        if (value is not None) and (not isinstance(value, str)):
            raise TypeError('Value must be a string')
        return value


class ElementDictNames(object):
    """Descriptor class to get a list of an ElementDict's members."""
    def __get__(self, instance, owner=None):
        return instance.members.keys()

    def __set__(self, instance, owner=None):
        """Raises an exception upon an attempt to modify; this is read-only."""
        raise AttributeError('Read-only attribute.')


class ElementDict(ElementAccess):
    """Container which provides access to a group of XML elements.

    Operates similar to a dictionary where a child element is referenced
    by index notation to find the child with the matching key attribute.
    Instead of returning the actual XML element, a member class is
    instantiated and returned which is used to handle access to the child's
    data.
    
    :param parent: Parent element that is associated with the dictionary
    :param key_attr: Attribute to be used as the dictionary key. If this is None then sequential numbers will be used.
    :param types: A dictionary used to look up the class to be used for a particular key. A single type can be supplied which will always the same type of class.
    :param type_attr: An attribute can be used to lookup the type of class to return. The value of the attribute will match the key of types.
    :param dfl_type: If the type cannot be found with the types dictionary, the default type will be returned.
    :param key_type: In the case where the primary key isn't a string, this is used to define it
    :param member_args: Additional parameters to pass to the constructor when returning the instance.
    :param use_tag_filter: Select only the child elements which have the this XML element name.
    :param tag_filter: Select only the child elements which have this XML element name.
    :param use_tagname: Use the element name to determine the type of object to return instead of *key_attr*
    :param attr_filter: select only the child elements that have this attribute
    """
    names = ElementDictNames()

    def __init__(self, parent, \
                 key_attr=None, \
                 types=None, \
                 type_attr=None, \
                 dfl_type=None,
                 key_type=str, \
                 member_args=[], \
                 tag_filter=None, \
                 use_tagname=False, \
                 attr_filter=None):
        ElementAccess.__init__(self, parent)
        self.types = types
        self.type_attr = type_attr
        self.dfl_type = dfl_type
        self.member_args = member_args
        self.use_tagname = use_tagname
       
        #Used to select elements based on their name
        m_elements = self.child_elements
        
        #When no optional arguments are used all child elements of current element
        if tag_filter is None and attr_filter is None:
            member_elements = m_elements
        
        #Selects all child elements with tag = *tag_filter* are selected
        if tag_filter is not None:
            member_elements = []
            for e in m_elements:
                if e.nodeName == tag_filter:
                        member_elements += [e]
                        
        #Selects all child elements that have the attribute *key_attr*            
        if attr_filter is not None:
            member_elements = []
            for e in m_elements:                
                if e.hasAttribute(key_attr):
                    member_elements += [e]                            
        
        #Generate sequential keys if no attribute key is available
        if key_attr is None:
            keys = tuple(str(y) for y in range(0,len(member_elements)))
        else: # 
            keys = [key_type(e.getAttribute(key_attr)) for e in member_elements]
        self.members = dict(zip(keys, member_elements))

    def __getitem__(self, key):
        """Return a member class suitable for accessing a child element."""
        try:
            element = self.members[key]
        except KeyError:
            raise KeyError("{0} not found".format(key))

        args = [element]
        args.extend(self.member_args)
        
        try:            
            return self.types(*args)
        except TypeError:
            if self.type_attr is not None:
                type_name = element.getAttribute(self.type_attr)
            elif self.use_tagname:                
                type_name = element.nodeName
            else:
                type_name = key            
            return self.types.get(type_name, self.dfl_type)(*args)

    def __delitem__(self, key):
        """Delete a child element by key"""
        try:
            element = self.members[key]
        except KeyError:
            raise KeyError("{0} not found".format(key))
        
        self.element.removeChild(element)
        
        #Delete item from internal dictionary
        del self.members[key]

    def __len__(self):
        count = 0
        for member in self.members:
            count += 1
        return count
    
    def append(self, key, value):
        self.members[key] = value
        
    def __iter__(self):        
        return iter(self.members)
