import os
from pathlib import Path


class DisplayablePath(object):
    # Credit to stack overflow abstrus
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
        if self.is_dir:
            files = next(os.walk(self.path))[2]
            return len(files)
        else:
            return 0

    @property
    def file_size(self):
        """Get the size of the file or, if it is a directory, the average size of files directly under it
        (excluding subdirectories)"""
        if self.is_dir:
            if self.file_count <= 0:
                return 0
            files = next(os.walk(self.path))[2]
            total_size = 0
            for file in files:
                file_path = Path.joinpath(self.path, Path(file))
                total_size += int(file_path.stat().st_size)  # check if file is path first?
            return int(total_size/self.file_count)   # approximate to the int
        else:
            return self.path.stat().st_size

    def add_stats(self, stat_dict, count=True, size=True):
        stat_dict['file_size'][self.path] = self.file_size
        stat_dict['file_count'][self.path] = self.file_count
        return stat_dict

    def display(self, get_file_count=False, get_file_size=False):
        output = str(self.path.name)
        if self.path.is_dir():
            output += '/              '
            if get_file_count:
                output += '        File count = {!s}'.format(self.file_count)  # choose offset by checking the depth level?
            if get_file_size:
                output += '        Average File size = {!s} bytes'.format(self.file_size)

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
        """
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path for path in root.iterdir()), key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.generate_tree(path,
                                             parent=displayable_root,
                                             is_last=is_last,
                                             criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    def displayable(self, get_count=False, get_size=False):
        if self.parent is None:
            return self.display(get_file_count=get_count, get_file_size=get_size)

        _filename_prefix = (self.display_filename_prefix_last if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.display(get_file_count=get_count, get_file_size=get_size))]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))