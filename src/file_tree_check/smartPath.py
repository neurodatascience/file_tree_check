from pathlib import Path
from abc import ABC, abstractmethod


class SmartPath(ABC):
    """A SmartPath object is tied to a singular path (file or directory) and allows itself to be printed
    in a readable format and allow retrieval of some statistics.

    Each instance stores their parent directory and their depth relative to the first path.

    This is an abstract class for both files and folder Paths.
    """
    # Credit to stack overflow abstrus for the visual part

    # The separators for the visual representation of the file structure
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_smart_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_smart_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    def add_stats(self, stat_dict, identifier, measures=()):
        for measure in measures:
            if identifier not in stat_dict[measure]:
                stat_dict[measure][identifier] = dict()

        if "file_size" in measures:
            stat_dict["file_size"][identifier][self.path] = self.file_size
        if "file_count" in measures:
            stat_dict["file_count"][identifier][self.path] = self.file_count
        if "dir_count" in measures:
            stat_dict["dir_count"][identifier][self.path] = self.dir_count
        if "modified_time" in measures:
            stat_dict["modified_time"][identifier][self.path] = self.modified_time
        return stat_dict

    @property
    def file_size(self):
        return int(self.path.stat().st_size)

    @property
    def modified_time(self):
        return int(self.path.stat().st_mtime)

    @abstractmethod
    def file_count(self):
        raise NotImplementedError()

    @abstractmethod
    def dir_count(self):
        raise NotImplementedError()

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

        # Now that the display for the current directory is ready, we need to add
        # the separator for each target_depth level
        parent = self.parent
        # Going up the parent hierarchy
        while parent and parent.parent is not None:
            # If the parent was last in it's directory, the separator is '   ' otherwise it is '│   '
            parts.append(self.display_parent_prefix_middle if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        # Putting it all together in a single string
        return ''.join(reversed(parts))