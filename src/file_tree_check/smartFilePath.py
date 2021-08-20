import logging
from smartPath import SmartPath
import time

module_logger = logging.getLogger("file_tree_check.{}".format(__name__))


class SmartFilePath(SmartPath):
    """
    The Child class of SmartPath for path pointing to a file.
    """

    def get_identifier(self, stat_dict, separator="_"):
        """We identify file type by removing the subject number, which is the text before the first "_"
         and adding the parent folder name in front"""
        if separator not in self.path.name and self.path.name[-1] != separator:
            # if the file name does not contain nor finishes by the separator character, the full name is used
            file_identifier = self.parent.path.name + "/" + self.path.name
        else:
            # if the file name contain (and does not finish by) the separator,
            # everything before the first separator is removed
            file_identifier = self.parent.path.name + "/" + "".join(self.path.name.split(separator)[1:])
        return file_identifier

    @property
    def file_count(self):
        """Since this is not a directory, this measure is meaningless and the return None
        is handled by the calling function. """
        return None

    @property
    def dir_count(self):
        """Since this is not a directory, this measure is meaningless and the return None
        is handled by the calling function. """
        return None

    def display(self, measures=(), name_max_length=60):
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += 'File size = {!s} bytes'.format(self.file_size).ljust(40)
        if "modified_time" in measures:
            output += 'Modification time = {!s}'.format(time.ctime(self.modified_time)).ljust(60)
        return output + '\n'