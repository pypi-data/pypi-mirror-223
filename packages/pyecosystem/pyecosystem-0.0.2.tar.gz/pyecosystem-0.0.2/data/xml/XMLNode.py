import json
import XMLPath


class XMLNode:
    def __init__(self, tag, attributes={}, text="", namespaces={}, parent=None):
        self.tag = tag
        self.namespaces = namespaces
        self.attributes = attributes
        self.text = text
        self.tail = None  # not implemented
        self.parent = parent
        self.children = []

    def __str__(self):
        """
        Returns a simple xml string representation of the object.
        """
        return f'<{self.tag} attributes={self.attributes}>{self.text}</{self.tag}>'

    def __repr__(self):
        """
        Returns a class string representation of the XMLNode object.
        """
        return f'XMLNode(tag="{self.tag}", attributes={self.attributes}, text="{self.text}", namespaces={self.namespaces})'

    def __add__(self, other):
        """
        Adds `other` to the current instance's children if it is a XMLNode, if it is a string it will be appended to text attribute of the instance.

        Parameters:
            other (XMLNode or str): The object to add to the current instance's children.

        Returns:
            XMLNode: The modified instance after adding `other`.

        Raises:
            TypeError: If `other` is neither an XMLNode nor a string.
        """
        if isinstance(other, (XMLNode, CommentNode, ProcessingInstructionNode, CDATANode)):
            other.parent = self
            self.add_child(other)
        elif isinstance(other, str):
            self.text += other
        else:
            raise TypeError(f"Cannot add {type(other)} to XMLNode.")
        return self

    def __sub__(self, other):
        """
        removes the given `other` from the current instance's children if it is a XMLNode, if it is a string it will be removed from text attribute of the instance.

        Args:
            other (XMLNode or str): The value to subtract from the current XMLNode.

        Returns:
            XMLNode: The resulting XMLNode after subtraction.

        Raises:
            TypeError: If the `other` parameter is neither an XMLNode nor a string.
        """
        if isinstance(other, (XMLNode, CommentNode, ProcessingInstructionNode, CDATANode)):
            other.parent = None
            self.remove_child(other)
        elif isinstance(other, str):
            self.text = self.text.replace(other, "")
        else:
            raise TypeError(f"Cannot subtract {type(other)} from XMLNode.")
        return self

    def __len__(self):
        """
        Return the number of children present in this object.
        """
        return len(self.children)

    def __contains__(self, item):
        """
        Check if the given item is contained within the children of this object.

        Parameters:
            item (any): The item to check for containment.

        Returns:
            bool: True if the item is found in the children, False otherwise.
        """
        return item in self.children

    def __iter__(self):
        """
        Returns an iterator object for the given list of children.

        :return: An iterator object.
        """
        return iter(self.children)

    def __getitem__(self, item: int):
        """
        Get the child at the given index.

        Args:
            item (int): The index of the child to get.

        Returns:
            XMLNode: The child at the given index.
        """
        return self.children[item]

    def __getitem__(self, item: str):
        """
        Get the value associated with the given item from attributes.

        Parameters:
            item (str): The key to look up in the attributes dictionary.

        Returns:
            Any: The value associated with the given item, or None if the item is not found.
        """
        return self.attributes.get(item, None)

    def __setitem__(self, item: int, value):
        if not isinstance(value, (XMLNode, CommentNode, ProcessingInstructionNode, CDATANode)):
            raise TypeError(
                f"Cannot set {item}, value must be an instance of either of (XMLNode, CommentNode, ProcessingInstructionNode,CDATANode).")
        if item >= len(self.children):
            raise IndexError(f"Cannot set {item}, index out of range.")
        if self.is_anscestor(value):
            raise ValueError(
                "Circular reference: The given child element is already an ancestor.")
        self.children[item] = value

    def __setitem__(self, item: str, value: str):
        """
        Set the value associated with the given item in attributes.

        Parameters:
            item (str): The key to look up in the attributes dictionary.
            value (Any): The value to set.
        """
        self.attributes[str(item)] = str(value)

    def clear(self):
        """
        Clears the state of the object except for the tag of element.

        Returns:
            None
        """
        self.text = ""
        self.namespaces = {}
        self.attributes = {}
        self.children = []
        self.parent = None

    def is_anscestor(self, other):
        """
        Check if the current XMLNode is an ancestor of the given XMLNode.

        Parameters:
            other (XMLNode): The XMLNode to check.

        Returns:
            bool: True if the current XMLNode is an ancestor of the given XMLNode, False otherwise.
        """
        parent = other.parent
        while parent:
            if parent == self:
                return True
            parent = parent.parent
        return False

    def from_node(self, node):
        """
        Assigns the attributes of the given XMLNode object to the current object.

        Parameters:
            node (XMLNode): The XMLNode object from which to assign attributes.

        Returns:
            None
        """
        if isinstance(node, XMLNode) and isinstance(self, XMLNode):
            self.tag = node.tag
            self.namespaces = node.namespaces
            self.attributes = node.attributes
            self.text = node.text
            self.tail = node.tail
            self.parent = node.parent
            self.children = node.children
        else:
            raise TypeError("Cannot copy from a non-XMLNode object.")

    def get_text(self):
        """
        Get the text of the element.

        Returns:
            The text of the element.
        """
        return self.text

    def get_tail(self):
        """
        Get the tail of the element.
        If the element is created from an XML file, the text attribute holds either the text between the element’s start tag and its first child or end tag, or None, and the tail attribute holds either the text between the element’s end tag and the next tag, or None. For the XML data
        <a><b>1<c>2<d/>3</c></b>4</a>
        the a element has None for both text and tail attributes, the b element has text "1" and tail "4", the c element has text "2" and tail None, and the d element has text None and tail "3"

        Returns:
            The tail of the element.
        """
        return self.tail

    def get_attributes(self):
        """
        Get all the attributes of the element.

        Returns:
            A dictionary of all the attributes.
        """
        return self.attributes

    def get_attribute(self, attribute_name):
        """
        Get the value of the specified attribute.

        Parameters:
            attribute_name (str): The name of the attribute to retrieve.

        Returns:
            The value of the attribute, or None if it does not exist.
        """
        # return self.get_attributes().get(attribute_name)
        return self[attribute_name]

    def add_attribute(self, attribute_name, attribute_value):
        """
        Add an attribute to the object.

        Parameters:
            attribute_name (str): The name of the attribute.
            attribute_value (Any): The value of the attribute.

        Raises:
            Exception: If the attribute already exists.

        Returns:
            None
        """
        # if not self.get_attribute(attribute_name):
        #     self.attributes[attribute_name] = attribute_value
        if not self[attribute_name]:
            self[attribute_name] = attribute_value
        else:
            raise Exception(f"Attribute '{attribute_name}' already exists.")

    def update_attribute(self, attribute_name, new_value):
        """
        Update the value of an attribute in the element.

        Parameters:
        - attribute_name (str): The name of the attribute to update.
        - new_value (Any): The new value to assign to the attribute.

        Raises:
        - Exception: If the attribute does not exist in the element.

        Returns:
        - None
        """
        if self[attribute_name]:
            self[attribute_name] = new_value
        else:
            raise Exception(
                f"Attribute '{attribute_name}' not found in element '{self.tag}'.")

    def add_child(self, child):
        """
        Sets the parent of the given `child` to `self` and appends it to the list of children.

        :param child: The child object to add.
        :type child: Any
        :return: None
        """
        if self.is_anscestor(child):
            raise ValueError(
                "Circular reference: The given child element is already an ancestor.")
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        """
        Remove a child from the list of children.

        Parameters:
            child (any): The child object to be removed.

        Returns:
            None
        """
        child.parent = None
        return self.children.remove(child)

    def get_child(self, tag):
        """
        Find and return first child node with a specific tag.

        Parameters:
            tag (str): The tag of the child node to find.

        Returns:
            child: The first child node with the specified tag, if found. Otherwise, None.
        """
        if isinstance(tag, str):
            for child in self.children:
                if child.tag == tag:
                    return child
        else:
            raise TypeError("tag must be a string.")

    def get_children(self, tag=""):
        """
        Get the children of the current object.

        Parameters:
            tag (str): The tag to filter the children by. Default is an empty string.

        Returns:
            list: A list of children objects filtered by the given tag, if provided. Otherwise, returns all children objects.
        """
        if tag:
            return [child for child in self.children if child.tag == tag]
        return self.children

    def get_siblings(self, tag=""):
        """
        Get the siblings of the current element.

        :param tag: The tag name to filter the siblings by (optional).
        :type tag: str
        :return: A list of sibling elements.
        :rtype: list
        """
        if self.parent:
            return self.parent.get_children(tag)

        return []

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        return self

    def delete(self):
        """
        Delete the current node and all its children recursively.

        Returns:
        XMLNode: The deleted node.
        """
        for child in self.children:
            self.children.remove(child)
            trash = child.delete()
            del trash

        self.parent = None
        return self

    def iter(self, tag=None):
        """
        Iterates over the XML tree, yielding elements that match the given tag.

        :param tag: The tag to match elements against. If set to "*", matches all elements.
        :type tag: str or None
        :return: A generator that yields matching elements.
        :rtype: Iterator[Element]
        """
        if tag == "*":
            tag = None
        if tag is None or self.tag == tag:
            yield self
        for child in self:
            yield from child.iter(tag)

    def itertext(self):
        """
        Iterates over the text content of the element and its descendants in document order.

        Returns:
            A generator that yields the text content of the element and its descendants.
        """
        tag = self.tag
        if not isinstance(tag, str) and tag is not None:
            return
        t = self.text
        if t:
            yield t
        for child in self:
            yield from child.itertext()
            t = child.tail
            if t:
                yield t

    def find(self, path, namespaces=None):
        """
        Find an XML element by its path.

        Args:
            path (str): The path of the XML element to find.
            namespaces (dict, optional): A dictionary containing the XML namespaces used in the path. Defaults to None.

        Returns:
            The XML element found by the path.
        """

        return XMLPath.find(self, path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """
        Find the text value of the first element matching the specified XPath expression.

        Args:
            path (str): The XPath expression to search for.
            default (Optional[str]): The default value to return if no match is found. 
                Defaults to None.
            namespaces (Optional[dict]): A dictionary of namespace prefixes and 
                namespace URI mappings. Defaults to None.

        Returns:
            str: The text value of the first matching element, or the default value 
                if no match is found.
        """

        return XMLPath.findtext(self, path, default, namespaces)

    def findall(self, path, namespaces=None):
        """
        Find all elements in the XML document that match the specified path.

        Args:
            path (str): The XPath expression to search for.
            namespaces (dict, optional): A dictionary of namespace prefixes to namespace URIs.

        Returns:
            list: A list of Element objects that match the specified path.
        """

        return XMLPath.findall(self, path, namespaces)

    def iterfind(self, path, namespaces=None):
        """
        Find all matching elements in the XML document based on the given path and namespaces.

        :param path: The XPath expression to search for.
        :type path: str
        :param namespaces: A dictionary of namespace prefixes and URIs.
        :type namespaces: Optional[Dict[str, str]]
        :return: An iterator yielding the matching elements.
        :rtype: Iterator[xml.etree.ElementTree.Element]
        """

        return XMLPath.iterfind(self, path, namespaces)

    def to_dict(self):
        """
        Convert an Element to a dictionary. 

        Returns:
        dict: A dictionary representation of the Element, containing its tag, attributes, text, 
        namespaces, and children (if any).
        """
        data = {"tag": self.tag, "attributes": self.get_attributes(),
                "text": self.text, "namespaces": self.namespaces}
        if self.children:
            data["children"] = [child.to_dict() for child in self.children]
        return data

    def to_json(self):
        """
        Converts the XMLNode object to a JSON string.

        Returns:
            str: The JSON representation of the object.
        """
        return json.dumps(self.to_dict())

    def to_xml(self, indent="", newline=""):
        """
        Converts an XML element to a string representation, including all its attributes, namespaces, and children. 

        :param indent: (Optional) A string that is used to indent the XML element.
        :param newline: (Optional) A string that is used to represent a newline character.
        :return: A string containing the XML element and all its attributes, namespaces, and children.
        """
        if indent is None:
            indent = ""

        xml = f"{indent if self.parent else ''}<{self.tag}"
        for key, value in self.get_attributes().items():
            attribute_string = f' {key}="{value}"' if value else f' {key}'
            xml += attribute_string

        for prefix, uri in self.namespaces.items():
            if prefix:
                xml += f' xmlns:{prefix}="{uri}"'
            else:
                xml += f' xmlns="{uri}"'

        if not self.text and len(self.children) == 0:
            xml += f" />{newline}"
        else:
            xml += ">"
            if self.text:
                xml += f"{self.text}"
            if self.children:
                xml += f"{newline}"
            for child in self.children:
                xml += child.to_xml(indent + indent, newline=newline)

            xml += f"{indent if self.parent and self.children else ''}</{self.tag}>{newline}"
        return xml


class CommentNode:
    def __init__(self, text, parent=None):
        self.text = str(text)
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def get_text(self):
        return str(self.text)

    def set_text(self, text):
        self.text = str(text)

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def to_dict(self):
        return {"tag": "__comment__", "text": self.get_text()}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_xml(self, indent="", newline=""):
        return f"{indent}<!--{self.get_text()}-->{newline}"


class ProcessingInstructionNode:
    def __init__(self, target, data, parent=None):
        self.target = str(target)
        self.data = str(data)
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def get_target(self):
        return self.target

    def get_data(self):
        return self.data

    def set_target(self, target):
        self.target = str(target)

    def set_data(self, data):
        self.data = str(data)

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def to_dict(self):
        return {"tag": "__processing_instruction__", "target": self.target, "data": self.data}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_xml(self, indent="", newline=""):
        return f"{indent}<?{self.target} {self.data}?>{newline}"


class CDATANode:
    def __init__(self, text, parent=None):
        self.text = str(text)
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def get_text(self):
        return str(self.text)

    def set_text(self, text):
        self.text = str(text)

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        if isinstance(parent, XMLNode) or parent is None:
            self.parent = parent
        else:
            raise Exception("The parent must be an XMLNode object or None.")

    def to_dict(self):
        return {"tag": "__cdata__", "text": self.get_text()}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_xml(self, indent="", newline=""):
        return f"{indent}<![CDATA[{self.get_text()}]]>{newline}"
