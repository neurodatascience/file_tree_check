import logging
from smartPath import SmartPath
import time

module_logger = logging.getLogger("file_tree_check.{}".format(__name__))


class SmartFilePath(SmartPath):
    """
    The Child class of SmartPath for path pointing to a file.
    """

    def add_stats(self, stat_dict, measures=(), separator="_"):
        # We identify files type by removing the subject number, which is the text before the first "_"
        # and adding the parent folder name in front
        # if the file name did not contain or finishes by the separator character, the full name is used
        if separator not in self.path.name and self.path.name[-1] != separator:
            file_identifier = self.parent.path.name + "/" + self.path.name
        # if the file did contain the separator, everything before the first separator is removed
        else:
            file_identifier = self.parent.path.name + "/" + "".join(self.path.name.split(separator)[1:])
        if "file_size" in measures:
            if file_identifier not in stat_dict["file_size"]:
                stat_dict["file_size"][file_identifier] = dict()
            stat_dict["file_size"][file_identifier][self.path] = self.file_size
        if "modified_time" in measures:
            if file_identifier not in stat_dict["modified_time"]:
                stat_dict["modified_time"][file_identifier] = dict()
            stat_dict["modified_time"][file_identifier][self.path] = self.modified_time
        return stat_dict

    @property
    def file_size(self):
        return int(self.path.stat().st_size)

    @property
    def modified_time(self):
        return int(self.path.stat().st_mtime)

    def display(self, measures=(), name_max_length=60):
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += 'File size = {!s} bytes'.format(self.file_size).ljust(40)
        if "modified_time" in measures:
            output += 'Modification time = {!s}'.format(time.ctime(self.modified_time)).ljust(60)
        return output + '\n'