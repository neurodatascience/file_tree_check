from __future__ import annotations

import time

from smartPath import SmartPath


class SmartFilePath(SmartPath):
    """The Child class of SmartPath for files."""

    @property
    def file_count(self):
        """Since this is not a directory, this measure is meaningless and the return None \
        is handled by the calling function."""
        return None

    @property
    def dir_count(self):
        """Since this is not a directory, this measure is meaningless and the return None \
        is handled by the calling function."""
        return None

    def display(self, measures=(), name_max_length: int = 60) -> str:
        """Call the SmartPath display and add some relevant measures to be printed alongside it."""
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += f"File size = {self.file_size!s} bytes".ljust(40)
        if "modified_time" in measures:
            output += f"Modification time = {time.ctime(self.modified_time)!s}".ljust(60)
        return output + "\n"
