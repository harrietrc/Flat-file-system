__author__ = 'Harriet Robinson-Chen'
__project__ = 'Softeng 370 Assignment 2'

import sys
import os

def main():
    fs = FileSystem()
    while True:
        line = fs.prompt()
        fs.parse(line)


class FileSystem(object):

    file_tree = None

    def __init__(self):
        self.file_tree = FileTree()

    def prompt(self):
        var = input("ffs>")
        return var

    def interpret(self, command, args):
        """ Executes the method to be called based on user input. Returns the not_mapped method (command not found) if
            the input is invalid. Decided to execute here rather than in main to make it easier to unit test.
        """
        if len(args):  # Arguments were given
            {'create':self.create}.get(command, self.not_mapped)(args)
        else: # No arguments given
            {'quit':self.quit, 'tree':self.tree}.get(command, self.not_mapped)()

    def not_mapped(self, args=None):
        print("Invalid command. Please try again.")

    def parse(self, line):
        """ Converts the user's input into command and arguments
        """
        command, space, args = line.partition(' ')
        self.interpret(command, args) # Not sure if it should be called from here

    def create(self, file_name):
        """ Creates a file with the specified name
        """
        # Check that the file name is valid
        if self.validate_create(file_name):
            file = open(file_name, 'w') # Doesn't really need to be in the if block, as only opens and closes the file
            file.close()
            self.file_tree.create_file_by_name(file_name)

    # Also needs to add the new file to the tree - could separate by leaving that up to the scan function - separation
    # of concerns. But needs to check for uniqueness (should be property of set)

    def validate_create(self, file_name):
        """ Validates that the file name is valid. If it is, this returns true. Should test both that the file is not
            a directory and that it is unique.
        """
        if file_name[-1] == '-':
            print("Directories should not be created directly.")
            return False

        # Check that file name is unique
        for file in os.listdir('.'):
            if file == file_name:
                print("File name is not unique")
                return False

        return True

    def tree(self):
        """ Print the file tree
        """
        print(self.file_tree)

    def quit(self):
        sys.exit()

""" Tree stuff """


class FileTree(object):
    """ This tree is only a representation of the file tree. It shouldn't be used to modify the actual
        file system. Will translate between fully-qualified names and the node representation. Singleton?
    """
    def __init__(self):
        self.root = DirNode(None, "-", None, None)  # The root node will always have no parent and be named '-'
        self.current_directory = self.root

    def __str__(self):
        s = ''
        s += str(self.root)
        return s

    def is_current_directory_valid(self):
        """ Tests whether the current directory exists in the file tree.
        """
        pass

    def locate_by_name(self, name):
        """ Locates a file or directory by name and returns that node. Throws an exception if the node is not found.
            Expects the absolute path at the moment.
        """
        # Things screw up if you don't account for this case
        if name == '-':
            return self.root

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
            path_length = len(name_path) -1
        else:
            is_dir = True
            target = name_path[-2]
            path_length = len(name_path) - 2

        if not path_length:
            node = self.root  # Parent is root
        else:
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
                if d.name == target:  # fix this as below
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

    # ABS ONLY!!
    def create_file_by_name(self, name):
        """ Given the fully-qualified name of a file, creates that file
        """
        path = name.split('-')
        absolute_paths = ["-".join(path[:x]) + '-' for x in range(2,len(path))]  # Excludes the root directory

        if not path[0]:  # Absolute
            for directory in absolute_paths:  # All the directories in the path
                self.create_dir_by_name(directory)  # Should probably check for existence in tree)

        rel_name = path[-1]
        parent = self.get_parent(name)
        self.add_file_to_parent(rel_name, parent)

    def create_dir_by_name(self, name):
        """ Given the fully-qualified name of a directory, creates that directory
        """
        rel_name = name.split('-')[-2]
        parent = self.get_parent(name)
        self.add_dir_to_parent(rel_name, parent)

    def add_dir_to_parent(self, dir_name, parent):
        """ Adds a directory (specified with its name relative to the parent) to a given parent node.
        """
        new_child = DirNode(parent, dir_name, None, None)  # Directory has no children at the moment
        parent.add_child_dir(new_child)
        return new_child

    def add_file_to_parent(self, file_name, parent):
        """ Adds a file (specified with its name relative to the parent) to a given parent node.
        """
        new_child = FileNode(parent, file_name)
        parent.add_child_file(new_child)
        return new_child

    def get_parent(self, name):
        """ Gets the parent as a node from the child's fully-qualified name
        """
        # If we're asked for the parent of the root node, just return the root
        if name == '-':
            return self.root

        # Get the path, excluding the child, and use it to find the parent.
        if name[-1] == '-':  # Directory
            path = name.rsplit('-', 2)[0]
            path_to_parent = '-' if not path else path + '-'
            parent = self.locate_by_name(path_to_parent)
        else:  # File
            path = name.rsplit('-', 1)[0]
            path_to_parent = '-' if not path else path + '-'
            parent = self.locate_by_name(path_to_parent)
        return parent

    def scan(self, directory):
        """ Scans the given directory for new files and directories that were not created through this program.
        """
        pass


class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __hash__(self):
        return hash((self.name,self.parent))

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

    def __hash__(self):
        return super(FileNode, self).__hash__()

    def __str__(self):
        s = '\t' + self.parent.name + '\n' # not actually what we want but it'll do for now
        s +='\t' + self.name + '\n'
        return s


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

    def __hash__(self):
        return super(DirNode, self).__hash__()

    def __str__(self):
        s = self.name + '\n'
        s += '\t\n'.join(map(str, self.files))
        s += '\t\n'.join(map(str, self.dirs))
        return s


class NoSuchPathException(Exception):
    pass

if __name__ == "__main__":
    main()