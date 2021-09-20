from smartPath import SmartPath
import time


class SmartFilePath(SmartPath):
    """The Child class of SmartPath for files.
    """

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
        """Call the SmartPath display and add some relevant measures to be printed alongside it."""
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += 'File size = {!s} bytes'.format(self.file_size).ljust(40)
        if "modified_time" in measures:
            output += 'Modification time = {!s}'.format(time.ctime(self.modified_time)).ljust(60)
        return output + '\n'