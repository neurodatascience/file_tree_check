from pathlib import Path
from abc import ABC, abstractmethod


class SmartPath(ABC):
    """A SmartPath object is tied to a singular path (file or directory) and allows itself to be printed
    in a readable format and allow retrieval of some statistics.

    While each instance is for a single file or directory, the method generate_tree() allows to recursively generate an
    instance for every file and folder in a given directory.

    Each instance stores their parent directory and their depth relative to the first path.

    This is an abstract class for both files and folder Paths.
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
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @abstractmethod
    def add_stats(self, stat_dict, measures=(), separator="_"):
        pass

    @classmethod
    def default_criteria(cls, path):
        return True

    def display(self, measures=(), name_max_length=60):
        return str(self.path.name).ljust(name_max_length - self.depth * 3)

    def displayable(self, measures=(), name_max_length=60):
        """Returns a str corresponding to a single line in the file structure visualisation."""
        # If the path is the root, no separators are needed at the beginning of the line
        if self.parent is None:
            return self.display(measures, name_max_length)

        # If the path is the last in it's directory, it will begin with └── instead of ├──"
        _filename_prefix = (self.display_filename_prefix_last if self.is_last
                            else self.display_filename_prefix_middle)

        # Display the info about the file/folder after the prefix chose above
        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.display(measures, name_max_length))]

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