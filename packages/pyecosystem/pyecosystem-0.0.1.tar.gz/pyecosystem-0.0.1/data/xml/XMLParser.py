import json
from XMLNode import XMLNode, CommentNode, ProcessingInstructionNode, CDATANode
from XMLTree import XMLTree


class XMLParser:
    def __init__(self):
        self.tree = XMLTree(root_tag="__ROOT__")
        self.root = self.tree.root
        self.current = None
        self.namespaces = {}
        self.stack = []

    def from_string(self, xml_string):
        """
        Parses an XML string and returns an XMLTree object.

        Args:
            xml_string (str): A string containing XML.

        Returns:
            XMLTree: The parsed XML tree.

        """

        self.__init__()
        index = 0
        while index < len(xml_string):
            # check if it is starting tag indicator
            if xml_string[index] == "<":

                # check if it is comment
                if xml_string[index:index + 4] == "<!--":
                    comment_end = xml_string.find("-->", index + 4)
                    if comment_end != -1:
                        comment_text = xml_string[index + 4:comment_end]
                        if comment_text and self.current:

                            comment = CommentNode(comment_text, self.current)
                            self.current.add_child(comment)

                        index = comment_end + 3
                        continue

                # check if it is processing instruction
                if xml_string[index:index + 2] == "<?":
                    processing_instruction_end = xml_string.find(
                        "?>", index + 2)
                    if processing_instruction_end != -1:
                        pi_text = xml_string[index +
                                             2:processing_instruction_end]
                        target = pi_text.split(" ")[0]
                        data = " ".join(pi_text.split(" ")[1:])
                        if pi_text and self.current:

                            pi = ProcessingInstructionNode(
                                target=target, data=data, parent=self.current)
                            self.current.add_child(pi)
                        index = processing_instruction_end + 2
                        continue

                # check if it is CDATA section
                if xml_string[index:index + 9] == "<![CDATA[":
                    cdata_end = xml_string.find("]]>", index + 9)
                    if cdata_end != -1:
                        text = xml_string[index+9:cdata_end]

                        if text and self.current:
                            cdata = CDATANode(text, self.current)
                            self.current.add_child(cdata)
                            # if self.current.text:
                            #     self.current.text += text
                            # else:
                            #     self.current.text = text

                        index = cdata_end + 3
                        continue

                # check if it is closing tag indicator
                if xml_string[index + 1] == "/":
                    end_index = xml_string.find(">", index + 1)
                    tag = xml_string[index + 2:end_index]
                    tag_parts = tag.split(":")
                    self.namespaces = {}  # No namespace prefix
                    if len(tag_parts) > 1:
                        namespace_prefix = tag_parts[0]
                        tag = tag_parts[1]
                        self.namespaces[namespace_prefix] = namespace_prefix

                    # end the element and retrieve element from the stack to process
                    if self.current is not None and self.current.tag == tag:
                        if self.stack:
                            self.current = self.stack.pop()
                        else:
                            self.current = None
                    index = end_index + 1

                # process the element from opening tag and create nodes
                else:
                    # get opening tag name
                    end_index = xml_string.find(">", index + 1)
                    tag_end = xml_string.find(" ", index + 1, end_index)
                    if tag_end == -1:
                        tag_end = end_index

                    tag = xml_string[index + 1:tag_end]

                    # get namespaces / prefix
                    tag_parts = tag.split(":")
                    self.namespaces = {}  # No namespace prefix
                    if len(tag_parts) > 1:
                        namespace_prefix = tag_parts[0]
                        tag = tag_parts[1]
                        self.namespaces[namespace_prefix] = namespace_prefix

                    # get attributes
                    attributes = {}
                    attr_start = tag_end + 1
                    attr_end = xml_string.find(">", tag_end)
                    if attr_start < attr_end:
                        attr_string = xml_string[attr_start:attr_end].strip()
                        parts = attr_string.split(" ")
                        for i in range(0, len(parts)):
                            pair = parts[i].split("=")
                            if len(pair) > 1:
                                key = pair[0]
                                value = pair[1].strip("\"")
                                # check if it is a namespaces or attributes
                                if key.startswith("xmlns:"):
                                    self.namespaces[key.replace(
                                        "xmlns:", "")] = value
                                elif key == "xmlns":
                                    self.namespaces[''] = value
                                else:
                                    attributes[key] = value

                    # create node from extracted data
                    node = XMLNode(tag=tag, attributes=attributes,
                                   namespaces=self.namespaces)

                    # check if we have any current node set, if not means we are at root
                    if self.current is None:
                        self.root.from_node(node)
                    # if we have a current node, add newly created node as current node's child and add current node to the stack
                    else:
                        self.current.add_child(node)
                        self.stack.append(self.current)

                    # set current node to be the newly created node
                    self.current = node

                    # check if it is self closing tag
                    if xml_string[attr_end - 1] == "/":
                        if self.stack:
                            self.current = self.stack.pop()
                        else:
                            self.current = None

                    index = attr_end
            # processing for text data
            else:
                text_end = xml_string.find("<", index)
                text = xml_string[index:text_end].strip()
                # check if we have any current node set, then add text to current node
                if self.current is not None and text:
                    if self.current.text is None:
                        self.current.text = text
                    else:
                        self.current.text += text
                index = text_end - 1

            # increment index
            index += 1

        return self.tree

    def from_file(self, file_path):
        """
        Reads an XML file from the given file path and returns the parsed XML data.

        :param file_path: A string representing the path to the XML file to be parsed.
        :type file_path: str

        :return: The parsed XML Tree Object.
        :rtype: XMLTree
        """
        with open(file_path, "r") as file:
            xml_string = file.read()
        return self.from_string(xml_string)

    def from_stream(self, stream):
        """
        Reads an XML file from the given stream and returns the parsed XML data.

        :param stream: A readable stream object representing the XML to be parsed.
        :type stream: any

        :return: The parsed XML Tree Object.
        :rtype: XMLTree
        """
        xml_string = stream.read()
        return self.from_string(xml_string)

    def from_dict(self, data):
        """
        Parses a dictionary and converts it into an XML string.

        Args:
            data (dict): The dictionary to be converted.

        Returns:
            XMLTree: The parsed XML tree object.
        """
        self.__init__()
        self.tree.from_dict(data)
        return self.tree

    def from_json(self, data):
        """
        Parses a JSON string and converts it into an XML string.

        Args:
            data (str): The JSON string to be converted.

        Returns:
            XMLTree: The parsed XML tree object.
        """
        return self.from_dict(json.loads(data))
