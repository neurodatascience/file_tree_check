import os
import logging
from pathlib import Path
from smartPath import SmartPath

module_logger = logging.getLogger("file_tree_check.{}".format(__name__))


class SmartDirectoryPath(SmartPath):
    """
    The Child class of SmartPath for path pointing to a directory.
    """

    def add_stats(self, stat_dict, measures=(), separator="_"):
        dir_name = self.path.name  # stats are saved with folder name ("anat", "sub-..") for comparison
        if "file_count" in measures:
            if dir_name not in stat_dict["file_count"]:
                stat_dict["file_count"][dir_name] = dict()
            stat_dict["file_count"][dir_name][self.path] = self.file_count

        if "dir_count" in measures:
            if dir_name not in stat_dict["dir_count"]:
                stat_dict["dir_count"][dir_name] = dict()
            stat_dict["dir_count"][dir_name][self.path] = self.dir_count
        return stat_dict

    @property
    def file_size(self):
        """The size of the file or, if it is a directory, the average size of files directly under it
                (excluding subdirectories)"""
        if self.file_count <= 0:
            return 0
        # Using a single run of os.walk to get only the files directly under the path
        files = next(os.walk(self.path))[2]
        total_size = 0
        for file in files:
            file_path = Path.joinpath(self.path, Path(file))
            total_size += int(file_path.stat().st_size)  # check if file is path first?
        return int(total_size / self.file_count)  # approximating to the int
        # this way of checking the size is not the most efficient since a directory will recheck every of its file size
        # even if these files already know their own size because they were checked first

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
        if "dir_count" in measures:
            output += 'Directory count = {!s}'.format(self.dir_count).ljust(40)
        if "file_count" in measures:
            output += 'File count = {!s}'.format(self.file_count).ljust(40)
        return output + '\n'