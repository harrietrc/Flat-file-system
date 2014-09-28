__author__ = 'Harriet Robinson-Chen - hrob748'
__project__ = 'Softeng 370 Assignment 2'

""" One thing to note, if this doesn't behave as expected - any files you manually add (outside of through the create
    command) will be picked up by this file system if they're formatted like the other ffs files. I didn't, however,
    implement a check to see whether files had been removed by means other than the delete command.

    Note also that dd, tree, and ls accept directory names that miss the final hyphen, even though the specs don't
    require it (although I think it might be mentioned somewhere on the assignment brief).
    """

import sys
import os


def main():
    # Get the input function for this version of Python
    if sys.version[0] == '3':
	raw_input = input

    # Create the directory, if necessary
    if not os.path.exists('./A2dir'):
        os.makedirs('./A2dir')

    # Prompt and execute
    fs = FileSystem()
    while True:
        fs.scan()
        line = fs.prompt()

	# Simulate user input if the input is redirected from a file
        if not os.isatty(sys.stdin.fileno()): 
            print(line)

        fs.parse(line)


class FileSystem(object):

    file_tree = None

    def __init__(self):
        self.file_tree = FileTree()

    def prompt(self):
        var = raw_input("ffs> ")
        return var

    def interpret(self, command, args):
        """ Executes the method to be called based on user input. Returns the not_mapped method (command not found) if
            the input is invalid. Decided to execute here rather than in main to make it easier to unit test.
        """
        if len(args):  # Arguments were given
            {'create': self.create, 'delete': self.delete, 'ls': self.ls, 'dd': self.dd, 'add': self.add,
                'cat': self.cat, 'cd': self.cd, 'tree': self.tree}.get(command, self.not_mapped)(args)
        else:  # No arguments given
            {'quit': self.quit, 'tree': self.tree, 'ls': self.ls, 'rls': self.rls, 'clear': self.clear, 'pwd': self.pwd,
                'cd': self.cd}.get(command, self.not_mapped)()

    def not_mapped(self, args=None):
        print("Invalid command. Please try again.")

    def parse(self, line):
        """ Converts the user's input into command and arguments
        """
        command, space, args = line.partition(' ')
        self.interpret(command, args)  # Not sure if it should be called from here

    def create(self, file_name):
        """ Creates a file with the specified name
        """
        # A better design would call this in some function in the FileTree class. Converts relative to absolute.
        if file_name[0] != '-':
            file_name = self.file_tree.relative_to_absolute(file_name)

        # Check that the file name is valid
        if self.validate_create(file_name):
            file = open('./A2dir/' + file_name, 'w')
            file.close()
            self.file_tree.create_file_by_name(file_name)

    def delete(self, file_name):
        """ Deletes the file with the specified name
        """
        # A better design would call this in some function in the FileTree class. Converts relative to absolute.
        if file_name[0] != '-':
            file_name = self.file_tree.relative_to_absolute(file_name)

        # Check that the file exists
        if self.validate_delete(file_name):
            os.remove('./A2dir/' + file_name)
            self.file_tree.delete_file_by_name(file_name)

    def dd(self, dir_name):
        """ Deletes the directory with the specified name.
        """
        # Allow the user to leave off the final hyphen
        if dir_name[-1] != '-':
            dir_name += '-'

        # A better design would call this in some function in the FileTree class. Converts relative to absolute.
        if dir_name[0] != '-':
            dir_name = self.file_tree.relative_to_absolute(dir_name)

        # Check that directory exists
        if self.validate_dd(dir_name):
            for file in os.listdir('./A2dir'):
                if file.startswith(dir_name):
                    os.remove('./A2dir/' + file)  # Delete the actual file
            self.file_tree.delete_dir_by_name(dir_name)  # Delete the representation of the directory from the tree

    def clear(self):
        """ Deletes all the files in root (directories cannot stand on their own). Will only delete files that are
            part of the ffs (i.e. start with '-')
        """
        for file in os.listdir('./A2dir'):
            if file.startswith('-'):  # I have my git files, and of course this .py file in there
                os.remove('./A2dir/' + file)
            # Clear the tree
            self.file_tree = FileTree()  # Just replace the old tree

    def add(self, args):
        """ Parses arguments to file name and content to be appended, then appends the content to the file. Assumes
            that the file name has no spaces.
        """
        # It would have made more sense to do this line elsewhere, but this was simpler.
        file_name, space, content = args.partition(' ')

        # A better design would call this in some function in the FileTree class. Converts relative to absolute.
        if file_name[0] != '-':
            file_name = self.file_tree.relative_to_absolute(file_name)

        if self.file_exists(file_name):
            with open('./A2dir/' + file_name, 'a') as file:
                file.write(content)
        else:
            print("File does not exist.")

    def cat(self, file_name):
        """ Prints the contents of a named file. File names can be absolute or relative.
        """
        # A better design would call this in some function in the FileTree class. Converts relative to absolute.
        if file_name[0] != '-':
            file_name = self.file_tree.relative_to_absolute(file_name)

        if self.file_exists(file_name):
            with open('./A2dir/' + file_name) as file:
                content = file.read()
                print(content)
        else:
            print("File does not exist")

    def validate_dd(self, dir_name):
        """ Validates that the directory to be deleted exists. Returns false if the name is invalid.
        """
        # Check that it's actually a directory
        if dir_name[-1] != '-':
            print("Please enter a directory name, not the name of a file.")
            return False

        # Deals only with absolute paths
        for file in os.listdir('./A2dir'):
            if file.startswith(dir_name):
                return True
        print("Directory does not exist.")
        return False

    def validate_delete(self, file_name):
        """ Validates that the file to be deleted exists in the directory. Returns false if the name is invalid.
        """
        # Check that it's actually a file
        if file_name[-1] == '-':
            print("Please enter a file name, not the name of a directory.")
            return False

        # Deals with absolute paths only
        if self.file_exists(file_name):
            return True
        print("File does not exist.")
        return False

    def validate_create(self, file_name):
        """ Validates that the file name is valid. If it is, this returns true. Should test both that the file is not
            a directory and that it is unique.
        """
        if file_name[-1] == '-':
            print("Directories should not be created directly.")
            return False

        # Check that file name is unique
        if self.file_exists(file_name):
            print("File name is not unique")
            return False
        return True

    def file_exists(self, file_name):
        """ Checks whether the file exists in the current directory. Returns true if it does.
        """
        for file in os.listdir('./A2dir'):
            if file == file_name:
                return True
        return False

    def tree(self, dir_name=None):
        """ Print the file tree
        """
        if not dir_name:  # Print from the root down
            tree = str(self.file_tree)[:-1]
            print(tree)
        else:
            # Allow the user to leave off the final hyphen
            if dir_name[-1] != '-':
                dir_name += '-'

            # A better design would call this in some function in the FileTree class. Converts relative to absolute.
            if dir_name[0] != '-':
                dir_name = self.file_tree.relative_to_absolute(dir_name)

            try:
                tree = self.file_tree.print_tree_from_dir(dir_name)[:-1]
                print(tree)
            except NoSuchPathException:
                print("Directory does not exist.")

    def ls(self, dir_name=None):
        """ Lists all the files and directories in the specified directory, or in the current working directory if no
            directory is specified.
        """
        # No argument - use current working directory
        if not dir_name:
            dir_name = self.file_tree.current_directory.get_full_name()

        # Allow the user to leave off the final hyphen
        if dir_name[-1] != '-':
            dir_name += '-'

        directory = self.file_tree.locate_by_name(dir_name)

        # Print files and directories in specified directory
        for file in directory.files:
            print("f: " + file.name)
        for child_dir in directory.dirs:
            print("d: " + child_dir.name)

    def rls(self):
        """ Executes the system's ls -l command. Assumes current directory is A2dir, but can easily be specified.
        """
        os.system('ls -l ./A2dir')

    def scan(self):
        """ Scans the real directory for new files and directories that were not created through this program. This
            DOES NOT check whether any files are manually deleted during program execution (as I don't think that
            even what I have here is necessary, let alone that added functionality).
        """
        # Perhaps a little inelegant?
        for file in os.listdir('./A2dir'):
            if file.startswith('-'):
                try:
                    self.file_tree.locate_by_name(file)
                except NoSuchPathException:
                    self.file_tree.create_file_by_name(file)

    def pwd(self):
        """ Prints the current working directory's name.
        """
        current_directory = self.file_tree.current_directory
        # I'm not sure I like that Node methods can be called from this class. ls already does this, however.
        current_directory_name = current_directory.get_full_name()
        print(current_directory_name)

    def cd(self, directory=None):
        """ Change the current working directory. No arg = root. .. = parent directory. For now this can't deal with
            commands such as cd ..-somesibling
        """
        # Lots of conditions within conditions - consider refactoring for sanity's sake.
        if not directory:
            self.file_tree.current_directory = self.file_tree.root
        elif directory == '..':  # Change to parent
            if self.file_tree.current_directory.name == '-':  # Root has no parent
                print("Root directory has no parent.")
            else:
                self.file_tree.current_directory = self.file_tree.current_directory.parent
        else:
            # Check format of name - specs say to allow the last hyphen to be ommitted.
            if directory[-1] != '-':
                directory += '-'
            try:
                self.file_tree.current_directory = self.file_tree.locate_by_name(directory)
            except NoSuchPathException:
                print("Directory does not exist.")

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
        s += self.root.print_tree(0)
        return s

    def print_tree_from_dir(self, dir_name):
        """ Prints the tree, starting at a certain directory, given the name of the directory
        """
        directory = self.locate_by_name(dir_name)
        s = directory.print_tree(0)
        return s

    def locate_by_name(self, name):
        """ Locates a file or directory by name and returns that node. Throws an exception if the node is not found.
            Expects the absolute path at the moment.
        """
        # Things screw up if you don't account for this case
        if name == '-':
            return self.root

        # Deal with relative paths
        if name[0] != '-':
            name = self.relative_to_absolute(name)

        # Get start node
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

    def delete_file_by_name(self, name):
        """ Given the fully-qualified name of a file, deletes that file
        """
        file = self.locate_by_name(name)
        parent = file.parent
        parent.rem_child_file(file)

    def delete_dir_by_name(self, name):
        """ Given the fully-qualified name of a directory, deletes that directory
        """
        directory = self.locate_by_name(name)

        parent = directory.parent
        parent.rem_child_dir(directory)
        directory.parent = None  # Have to break reference from parent to child, and child to parent

        # Check to see whether the current directory still exists (kind of a hacky way of doing it)
        try:
            self.current_directory.get_full_name()
        except MalformedTreeException:
            self.current_directory = self.root

    # ABS ONLY!!
    def create_file_by_name(self, name):
        """ Given the fully-qualified name of a file, creates that file
        """
        path = name.split('-')
        absolute_paths = ["-".join(path[:x]) + '-' for x in range(2, len(path))]  # Excludes the root directory

        if not path[0]:  # Absolute
            for directory in absolute_paths:  # All the directories in the path
                self.create_dir_by_name(directory)  # Should probably check for existence in tree)

        rel_name = path[-1]
        parent = self.get_parent_from_name(name)
        self.add_file_to_parent(rel_name, parent)

    def create_dir_by_name(self, name):
        """ Given the fully-qualified name of a directory, creates that directory
        """
        rel_name = name.split('-')[-2]
        parent = self.get_parent_from_name(name)
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

    def get_parent_from_name(self, name):
        """ Gets the parent as a node from the child's fully-qualified name. This is used for files/dirs that don't
            already exist - hence why we can't just return the parent field of the child.
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

    def relative_to_absolute(self, name):
        """ Converts a relative file name to an absolute one, using the current working directory.
        """
        current_dir_name = self.current_directory.get_full_name()
        return current_dir_name + name


class Node(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __hash__(self):
        return hash((self.name, self.parent))

    def get_full_name(self):
        """ Gets the fully qualified name of the file or directory.
        """
        parents = list()
        node = self
        while node.parent:  # Get parent until you hit the root
            parents.append(node.name)
            node = node.parent
        if node.name != '-':  # Orphan node
            raise MalformedTreeException("Node is not attached to the root.")
        full_name = '-'.join(reversed(parents))
        return '-' + full_name


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
        return self.name

    def get_full_name(self):
        return super(FileNode, self).get_full_name()


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

    def get_full_name(self):
        name = super(DirNode, self).get_full_name()
        return name + ('-' if name != '-' else '')  # Bit of a messy way to do things

    def __hash__(self):
        return super(DirNode, self).__hash__()

    def print_tree(self, nesting_level):
        """ Function that is called recursively in order to print the tree. I've assumed that the number of equals signs
            should be the same as the length of the directory name, not the length of the longest file name in that
            directory.
        """
        # Root doesn't need hyphens either side
        if self.name != '-':
            s = '\t' * nesting_level + '-' + self.name + '-' + '\n'
            num_equals = len(self.name) + 2
        else:
            s = '\t' * nesting_level + self.name + '\n'
            num_equals = len(self.name)

        # Print equals signs
        s += '\t' * nesting_level + '=' * num_equals + '\n'

        # Print files and directories
        for file in self.files:
            s += '\t' * nesting_level + str(file) + '\n'
        for directory in self.dirs:
            s += directory.print_tree(nesting_level + 1)
        return s


class NoSuchPathException(Exception):
    pass


class MalformedTreeException(Exception):
    """ Possible a bad name for this, but should be thrown when the tree is not structured as expected.
    """
    pass

if __name__ == "__main__":
    main()
