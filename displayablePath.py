import os
from pathlib import Path

class DisplayablePath(object):
    """A DisplayablePath object is tied to a singular path (file or directory) and allows itself to be printed
    in a readable format and allow retrieval of some statistics.
    While each instance is for a single file or directory, the method generate_tree() allows to recursively generate an
    instance for every file and folder in a given directory.
    Each instance stores their parent directory and their depth relative to the first path.
    """
    # Credit to stack overflow abstrus

    # The separators for the visual representation of the file structure
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        self.is_dir = self.path.is_dir()
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def file_count(self):
        """For a directory, indicates how many files are directly under it. Does not count subdirectories or files
        contained in them. For a file, this is set to -1."""
        if self.is_dir:
            files = next(os.walk(self.path))[2]
            return len(files)
        else:
            return -1

    @property
    def file_size(self):
        """The size of the file or, if it is a directory, the average size of files directly under it
        (excluding subdirectories)"""
        if self.is_dir:
            if self.file_count <= 0:
                return 0
            # Using a single run of os.walk to get only the files directly under the path
            files = next(os.walk(self.path))[2]
            total_size = 0
            for file in files:
                file_path = Path.joinpath(self.path, Path(file))
                total_size += int(file_path.stat().st_size)  # check if file is path first?
            return int(total_size/self.file_count)   # approximating to the int
        else:
            return self.path.stat().st_size

    def add_stats(self, stat_dict, count=True, size=True):
        # Only get the file count from folders
        if self.is_dir:
            stat_dict['file_count'][self.path] = self.file_count
        # Only get the file size from files
        else:
            stat_dict['file_size'][self.path] = self.file_size
        return stat_dict

    def display(self, get_file_count=False, get_file_size=False):
        # We display the name and some statistics further in the line if asked
        output = str(self.path.name)
        # If a directory, get the number of files directly underneath and their average size
        if self.path.is_dir():
            output += '/              '
            if get_file_count:
                output += '        File count = {!s}'.format(self.file_count)  # TODO change offset by the depth level
            if get_file_size:
                output += '        Average File size = {!s} bytes'.format(self.file_size)
        # If a file, only get its size
        if self.path.is_file() and get_file_size:
            output += '                  File size = {!s} bytes'.format(self.file_size)
        return output+'\n'

    @classmethod
    def _default_criteria(cls, path):
        return True

    @classmethod
    def generate_tree(cls, root, parent=None, is_last=False, criteria=None):
        """Generator that creates a tree
        Returns an iterable of the file structure that can be used with display() over each element.
        When a subdirectory is found under the given path, will call another instance of this method with it as the root
        """
        root = Path(str(root))
        # A criteria could be used to ignore specific files or folder
        criteria = criteria or cls._default_criteria

        # Begin by generating the root path
        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        # Get a list of every files or folder in the root and iterate over them
        children = sorted(list(path for path in root.iterdir()), key=lambda s: str(s).lower())
        count = 1
        for path in children:
            # Check if this path is the last children in its parent's directory
            is_last = count == len(children)
            # If the children is a folder, another instance of the method is called and
            # its output is propagated up the generator
            if path.is_dir():
                yield from cls.generate_tree(path,
                                             parent=displayable_root,
                                             is_last=is_last,
                                             criteria=criteria)
            # If the children is a file, generate a single instance of DisplayablePath associated to its path
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    def displayable(self, get_count=False, get_size=False):
        """Returns a str corresponding to a single line in the file structure visualisation."""
        # If the path is the root, no separators are needed at the beginning of the line
        if self.parent is None:
            return self.display(get_file_count=get_count, get_file_size=get_size)

        # If the path is the last in it's directory, it will begin with └── instead of ├──"
        _filename_prefix = (self.display_filename_prefix_last if self.is_last
                            else self.display_filename_prefix_middle)

        # Display the info about the file/folder after the prefix chose above
        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.display(get_file_count=get_count, get_file_size=get_size))]

        # Now that the display for the current directory is ready, we need to add the separator for each depth level
        parent = self.parent
        # Going up the parent hierarchy
        while parent and parent.parent is not None:
            # If the parent was last in it's directory, the separator is '   ' otherwise it is '│   '
            parts.append(self.display_parent_prefix_middle if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        # Putting it all together in a single string
        return ''.join(reversed(parts))