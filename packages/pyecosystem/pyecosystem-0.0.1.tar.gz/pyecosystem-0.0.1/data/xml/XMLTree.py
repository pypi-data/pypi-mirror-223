import json
from XMLNode import XMLNode


class XMLTree:
    def __init__(self, root_tag="ROOT", namespaces={}, root_node=None):
        self.root = None
        self.namespaces = {}
        if root_node:
            self.root = root_node
            self.namespaces = root_node.namespaces
        else:
            self.root = XMLNode(tag=root_tag, namespaces=namespaces)
            self.namespaces = namespaces

    def __str__(self):
        """
        Convert the object to a string representation.

        :return: A string representation of the object.
        """
        return str(self.root)

    def __repr__(self):
        """
        Return a string representation of the object.
        """
        return repr(self.root)

    def __len__(self):
        """
        Returns the length of the root element.
        """

        return len(self.root)

    def __contains__(self, element):
        """
        Check if the given element is present in the root element.

        Args:
            element: The element to check for presence in the root element.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        return element in self.root

    def __iter__(self):
        """
        to iterate over root element.

        Returns:
            The root of the tree.
        """
        return self.root

    def from_dict(self, data):
        """
        Builds an XML tree from a dictionary.

        Args:
            data (dict): The dictionary to build the tree from.
        """
        if not isinstance(data, dict) or len(data) != 1:
            raise ValueError(
                "Invalid dictionary format for XML conversion. there should be only one key for each element and only one root element.")

        root_tag, root_data = next(iter(data.items()))
        self.root.tag = root_tag

        self.__build_children_from_dict(self.root, root_data)

    def __build_children_from_dict(self, parent, data):
        """
        Builds children elements from a dictionary.

        Args:
            parent (XMLNode): The parent element.
            data (dict): The dictionary containing child element data.
        """
        for tag, value in data.items():
            if isinstance(value, dict):
                child = XMLNode(tag=tag)
                parent.add_child(child)
                self.__build_children_from_dict(child, value)
            elif isinstance(value, list):
                for item in value:
                    child = XMLNode(tag=tag)
                    parent.add_child(child)
                    if isinstance(item, dict):
                        self.__build_children_from_dict(child, item)
                    else:
                        child.text = str(item)
            else:
                child = XMLNode(tag=tag, text=str(value))
                parent.add_child(child)

    def iter(self, tag=None):
        """
        Iterates over the elements in the XML tree rooted at this element. If `tag` is
        not `None` or is a string, only elements whose tag equals `tag` are returned. 

        Parameters:
            tag (str): The tag of the elements to be returned. If `tag` is not provided,
                all elements in the tree are returned.

        Returns:
            Iterator: An iterator that yields the elements in the XML tree rooted at this
                element that match the specified tag.
        """

        # assert self._root is not None
        return self.root.iter(tag)

    def find(self, path, namespaces=None):
        """
        Find a specific path within the XML document.

        Args:
            path (str): The path to the element(s) to find within the XML document.
            namespaces (dict, optional): A dictionary of namespace prefixes and URIs. Defaults to None.

        Returns:
            object: The result of the find operation.
        """

        # assert self._root is not None
        if path[:1] == "/":
            path = "." + path
        return self.root.find(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """
        Find the text at the specified path in the XML tree.

        Args:
            path (str): The XPath expression to search for.
            default (Any, optional): The default value to return if the path is not found. Defaults to None.
            namespaces (Dict[str, str], optional): A dictionary of namespace prefixes to namespace URIs. Defaults to None.

        Returns:
            str: The text content at the specified path, or the default value if the path is not found.
        """

        # assert self._root is not None
        if path[:1] == "/":
            path = "." + path
        return self.root.findtext(path, default, namespaces)

    def findall(self, path, namespaces=None):
        """
        Find all elements in the XML tree that match the given path.

        Args:
            path (str): The path to search for.
            namespaces (dict, optional): A dictionary of namespace prefixes to URIs.

        Returns:
            list: A list of Element objects that match the given path.
        """

        # assert self._root is not None
        if path[:1] == "/":
            path = "." + path
        return self.root.findall(path, namespaces)

    def iterfind(self, path, namespaces=None):
        """
        Find all elements in the tree with a given tag.

        Args:
            path (str): The path to search for. If the path starts with "/", it will
                be relative to the root element. Otherwise, it will be relative to the
                current element.
            namespaces (dict, optional): A dictionary mapping namespace prefixes to
                namespace URIs. Defaults to None.

        Returns:
            Iterator[Element]: An iterator over all elements matching the given path.
        """

        # assert self._root is not None
        if path[:1] == "/":
            path = "." + path
        return self.root.iterfind(path, namespaces)

    def add_child_at(self, element_path, tag, attributes={}, text="", namespaces={}):
        """
        Adds a child element to the specified parent element.

        :param element_path: A string representing the path to the parent element.
        :type element_path: str
        :param tag: A string representing the tag of the child element to add.
        :type tag: str
        :param attributes: A dictionary representing the attributes of the child element (default None).
        :type attributes: dict
        :param text: A string representing the text of the child element (default None).
        :type text: str
        :param namespaces: A dictionary representing the namespaces of the child element (default None).
        :type namespaces: dict
        :raises ValueError: If the parent element specified by the `element_path` parameter is not found in the XML tree.
        """
        parent = self.find_element_by_path(element_path)
        if parent is None:
            raise ValueError(
                f"Element '{element_path}' not found in the XML tree.")
        child = XMLNode(tag=tag, attributes=attributes,
                        text=text, namespaces=namespaces)
        parent.add_child(child)

    def remove_element_by_path(self, element_path):
        """
        Remove an element from the XML tree.

        Parameters:
            element_path (str): The path of the element to be removed.

        Raises:
            Exception: If the element is the root element.
            Exception: If the element is not found in the XML tree.
        """
        element = self.find_element_by_path(element_path)
        if element is not None:
            if element.parent is not None:
                element.delete()
            else:
                raise Exception("Cannot remove the root element.")
        else:
            raise Exception(
                f"Element '{element_path}' not found in the XML tree.")

    def to_dict(self):
        """
        Converts a tree to a dictionary representation.

        :return: The dictionary representation of the tree.
        :rtype: dict
        """
        return self.root.to_dict()

    def to_json(self):
        """
        Convert the tree object to a JSON string representation.

        Returns:
            str: The JSON string representation of the object.
        """
        return json.dumps(self.root.to_dict())

    def to_xml(self, indent="", newline=""):
        """
        Converts a tree to a string representation.

        :param indent: (Optional) The character string to use for each indentation level.
        :type indent: str

        :param newline: (Optional) The character string to use for newlines.
        :type newline: str

        :return: The string representation of the tree.
        :rtype: str
        """

        return self.root.to_xml(indent=indent, newline=newline)

    def save_to_file(self, file_path, indent="", newline=""):
        """
        Saves the XML tree to a file located at `file_path`.

        :param file_path: The path to the file to save the XML tree to.
        :type file_path: str
        :param indent: The string used for indents. If not specified, there will be no pretty printing.
        :type indent: str
        :param newline: The string used for newlines. Default is an empty string.
        :type newline: str
        :return: None
        """

        xml_string = self.root.to_xml(indent=indent, newline=newline)
        with open(file_path, 'w') as file:
            file.write(xml_string)
