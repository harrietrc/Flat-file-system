__author__ = 'Harriet Robinson-Chen'
__project__ = 'Softeng 370 Assignment 2'

import sys

tree = None

def main():
    tree = FileTree()
    while True:
        line = prompt()
        parse(line)

def prompt():
    var = input("ffs>")
    return var

def interpret(command, args):
    """ Executes the method to be called based on user input. Returns the not_mapped method (command not found) if the
        input is invalid. Decided to execute here rather than in main to make it easier to unit test.
    """
    if len(args): # Arguments were given
        {'create':create}.get(command, not_mapped)(args)
    else: # No arguments given
        {'exit':exit}.get(command, not_mapped)()

def not_mapped():
    print("Invalid command. Please try again.")

def parse(line):
    """ Converts the user's input into command and arguments
    """
    command, space, args = line.partition(' ')
    interpret(command, args) # Not sure if it should be called from here

def create(file_name):
    """ Creates a file with the specified name
    """

    if file_name[-1] == '-':
        print("Directories should not be created directly.")

    file = open(file_name, 'w') # Is write permission the right permission?
    file.close()

# Also needs to add the new file to the tree - could separate by leaving that up to the scan function - separation of
# concerns. But needs to check for uniqueness (should be property of set)

def validate_create(file_name):
    """ Validates that the file name is valid. If it is, this returns true.
    """


def exit():
    sys.exit()

""" Tree stuff """

class FileTree(object):
    """ This tree is only a representation of the file tree. It shouldn't be used to modify the actual
        file system. Singleton?
    """
    def __init__(self):
        self.root = DirNode(None, "-", None, None) # The root node will always have no parent and be named '-'
        self.current_directory = self.root

    def is_current_directory_valid(self):
        """ Tests whether the current directory exists in the file tree.
        """
        pass

    def locate_by_name(self, name):
        """ Locates a file or directory by name and returns that node. Throws an exception if the node is not found.
            Uses a basic BFS.
        """
        queue = [] # Directories to search
        queue.append(self.root)
        return None

    def scan(self, dir):
        """ Scans the given directory for new files and directories that were not created through this program.
        """
        pass

class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

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
    def __init__(self, parent, name, files, dirs):
        super(DirNode, self).__init__(parent, name)
        self.files = set(files) if files is not None else set() # The files in this directory.
        self.dirs = set(dirs) if dirs is not None else set() # The directories in this directory.
        """ I've separated children into files and directories so that searching for a directory doesn't require
            unnecessary equality checks against files, and vice versa. """

    def __eq__(self, other):
        if isinstance(other, DirNode):
            return self.name == other.name and self.parent == other.parent
        return NotImplemented

    def add_child_file(self, child_file):
        """ Adds a new child file for the node.
        """
        self.files.add(child_file)

    def add_child_dir(self, child_dir):
        """ Adds a directory as a child for the node.
        """
        self.dirs.add(child_dir)

    """ If we need to worry about moving directories this gets a lot more complicated """

    def rem_child_file(self, child_file):
        """ Removes a child file from the list of children. Expects a node, not a name.
        """
        try:
            self.files.remove(child_file)
        except ValueError:
            pass

    def rem_child_dir(self, child_dir):
        """ Removes a child directory from the list of children. Expects a node, not a name.
        """
        try:
            self.dirs.remove(child_dir)
        except ValueError:
            pass

if __name__=="__main__":
    main()