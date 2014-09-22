import abc

class FileSystem(object):
    def __init__(self):


class FileTree(object):
    """ This tree is only a representation of the file tree. It shouldn't be used to modify the actual
        file system.
    """
    def __init__(self, root):
        self.root = root # Will always have the name -

class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    # @abc.abstractmethod
    # def is_dir(self):
    #     """ Returns true if the node is a directory.
    #     """
    #     return

class FileNode(Node):
    def __init__(self, parent, name):
        super(FileNode, self).__init__(parent, name)

    def __eq__(self, other):
        """ Problem with this is that it will call recursively up the tree - which is ok, but inefficient.
            Might need testing.
        """
        if isinstance(other, FileNode):
            return self.name == other.name and self.parent == other.parent
        return NotImplemented

class DirNode(Node):
    def __init__(self, parent, name, children):
        super(DirNode, self).__init__(parent, name)
        self.children = set(children) # The children of this directory

    def __eq__(self, other):
        if isinstance(other, DirNode):
            return self.name == other.name and self.parent == other.parent
        return NotImplemented

    def add_child(self, new_child):
        """ Adds a new child for the node.
        """
        self.children.add(new_child) # Do we need to deal with duplicate file names?

    """ If we need to worry about moving directories this gets a lot more complicated """

    def rem_child(self, child):
        """ Removes a child node from the list of children. Expects a node, not a name.
        """
        try:
            self.children.remove(child)
        except ValueError:
            pass