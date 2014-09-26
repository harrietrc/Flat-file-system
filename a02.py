__author__ = 'Harriet Robinson-Chen'
__project__ = 'Softeng 370 Assignment 2'

import sys


def main():
    fs = FileSystem()
    while True:
        line = fs.prompt()
        fs.parse(line)


class FileSystem(object):

    tree = None

    def __init__(self):
        self.tree = FileTree()

    def prompt(self):
        var = input("ffs>")
        return var

    def interpret(self, command, args):
        """ Executes the method to be called based on user input. Returns the not_mapped method (command not found) if
            the input is invalid. Decided to execute here rather than in main to make it easier to unit test.
        """
        if len(args):  # Arguments were given
            {'create':self.create, 'test':self.test}.get(command, self.not_mapped)(self, args)
        else: # No arguments given
            {'exit':exit}.get(command, self.not_mapped)(self)

    def test(self, args):
        node = self.tree.locate_by_name(args)
        print(node.name)

    def not_mapped(self):
        print("Invalid command. Please try again.")

    def parse(self, line):
        """ Converts the user's input into command and arguments
        """
        command, space, args = line.partition(' ')
        self.interpret(command, args) # Not sure if it should be called from here

    def create(self, file_name):
        """ Creates a file with the specified name
        """
        if file_name[-1] == '-':
            print("Directories should not be created directly.")

        file = open(file_name, 'w') # Is write permission the right permission?
        file.close()

    # Also needs to add the new file to the tree - could separate by leaving that up to the scan function - separation
    # of concerns. But needs to check for uniqueness (should be property of set)

    def validate_create(self, file_name):
        """ Validates that the file name is valid. If it is, this returns true.
        """
        pass

    def exit(self):
        sys.exit()

""" Tree stuff """


class FileTree(object):
    """ This tree is only a representation of the file tree. It shouldn't be used to modify the actual
        file system. Will translate between fully-qualified names and the node representation. Singleton?
    """
    def __init__(self):
        self.root = DirNode(None, "-", None, None)  # The root node will always have no parent and be named '-'
        self.current_directory = self.root

    def is_current_directory_valid(self):
        """ Tests whether the current directory exists in the file tree.
        """
        pass

    def locate_by_name(self, name):
        """ Locates a file or directory by name and returns that node. Throws an exception if the node is not found.
        """
        # Get start node
        if name[0] != '-':  # Path must be relative
            node = self.get_start_of_relative_path(name)
        else:
            node = self.root  # Start at the root

        name_path = name.split('-')[1:]

        # Target is located differently depending on whether we're looking for a file or directory
        if name_path[-1]:  # We're looking for a file
            is_dir = False
            target = name_path[-1]
            path_length = len(name_path) - 1
        else:
            is_dir = True
            target = name_path[-2]
            path_length = len(name_path) - 2

        # Step through the tree, checking/matching names of directories as we go
        for i in range(path_length):
            for d in node.dirs:
                if d.name == name_path[i]:
                    node = d
                    break
            else:  # No break statement encountered
                raise NoSuchPathException("The path provided is invalid.")

        # Node should be the parent, so now we just need to search for the target file/dir
        if is_dir:
            for d in node.dirs:
                if d.name == target:
                    return d
        else:
            for file in node.files:
                if file.name == target:
                    return file

        # Should have returned by now
        raise NoSuchPathException("The specified file or directory does not exist.")

    def get_start_of_relative_path(self, rel_path):
        """
        """
        pass

    def create_by_name(self, name):
        """ Given the fully-qualified name of a file or directory, creates that file/directory
        """

    def get_parent(self, name):
        """ Gets the parent as a node from the child's fully-qualified name
        """
        # If we're asked for the parent of the root node, just return the root
        if name == '-':
            return self.root

        # Get the path, excluding the child, and use it to find the parent.
        if name[-1] == '-':  # Directory
            parent = self.locate_by_name(name.split('-')[:-2])
        else:  # File
            parent = self.locate_by_name(name.split('-')[:-1])
        return parent

    def scan(self, directory):
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
        self.files = set(files) if files is not None else set()  # The files in this directory.
        self.dirs = set(dirs) if dirs is not None else set()  # The directories in this directory.
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


class NoSuchPathException(Exception):
    pass

if __name__ == "__main__":
    main()