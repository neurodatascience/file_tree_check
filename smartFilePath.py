import logging
from smartPath import SmartPath

module_logger = logging.getLogger("file_tree_check.{}".format(__name__))


class SmartFilePath(SmartPath):
    """
    The Child class of SmartPath for path pointing to a file.
    """

    def add_stats(self, stat_dict, get_file_count=True, get_dir_count=True, get_size=True, separator="_"):
        # We identify files type by removing the subject number, which is the text before the first "_"
        # and adding the parent folder name in front
        if get_size:
            file_identifier = self.parent.path.name + "/" + "".join(self.path.name.split(separator)[1:])
            if file_identifier not in stat_dict["file_size"]:
                stat_dict["file_size"][file_identifier] = dict()
            stat_dict["file_size"][file_identifier][self.path] = self.file_size
        return stat_dict

    @property
    def file_size(self):
        return int(self.path.stat().st_size)

    def display(self, get_file_count=False, get_dir_count=False, get_file_size=False):
        output = str(self.path.name)
        # If a file, only get its size
        if get_file_size:
            output += '                  File size = {!s} bytes'.format(self.file_size)
        return output + '\n'