import os
import logging
from pathlib import Path
from smartPath import SmartPath

module_logger = logging.getLogger("file_tree_check.{}".format(__name__))


class SmartDirectoryPath(SmartPath):
    """
    The Child class of SmartPath for path pointing to a directory.
    """

    def get_identifier(self, stat_dict, separator="_"):
        """For a folder, stats are saved directly with the folder name ("anat", "sub-..") for comparison"""
        return self.path.name

    @property
    def file_count(self):
        """For a directory, indicates how many files are directly under it. Does not count subdirectories or files
                        contained in them."""
        files = next(os.walk(self.path))[2]
        return len(files)

    @property
    def dir_count(self):
        """The number of directory found directly under this one."""
        directories = next(os.walk(self.path))[1]
        return len(directories)

    def display(self, measures=(), name_max_length=60):
        # We display the name and some statistics further in the line if asked
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += 'File size = {!s} bytes'.format(self.file_size).ljust(40)
        if "dir_count" in measures:
            output += 'Directory count = {!s}'.format(self.dir_count).ljust(40)
        if "file_count" in measures:
            output += 'File count = {!s}'.format(self.file_count).ljust(40)
        return output + '\n'