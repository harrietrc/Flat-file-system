__author__ = 'Harriet Robinson-Chen'
__project__ = 'Softeng 370 Assignment 2'

import abc # Not necessary unless you uncomment that abstract method
import sys

def main():
    while True:
        var = prompt()
        interpret(var)

def prompt():
    var = input("ffs>")
    return var

def interpret(user_input):
    """ Executes the method to be called based on user input. Returns the not_mapped method (command not found) if the
        input is invalid. Decided to execute here rather than in main to make it easier to unit test.
    """
    {'exit':exit}.get(user_input, not_mapped)()

def not_mapped():
    print("Invalid command. Please try again.")

def parse():
    pass

def exit():
    sys.exit()

""" Actual OOP stuff """

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

if __name__=="__main__":
    main()