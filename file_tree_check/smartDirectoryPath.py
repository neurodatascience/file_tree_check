from __future__ import annotations

import os
from pathlib import Path

from file_tree import FileTree

from .smartPath import SmartPath


class SmartDirectoryPath(SmartPath):
    """The Child class of SmartPath for directories (folder)."""

    def __init__(
        self,
        path: Path,
        parent_smart_path: SmartPath | None,
        is_last: bool,
        file_tree: FileTree | None = None,
    ):
        self.children = []
        super().__init__(path, parent_smart_path, is_last, file_tree)

    @property
    def file_count(self) -> int:
        """For a directory, indicates how many files are directly under it.

        Does not count subdirectories or files contained in them.
        """
        files = next(os.walk(self.path))[2]
        return len(files)

    @property
    def dir_count(self) -> int:
        """The number of directory found directly under this one."""
        directories = next(os.walk(self.path))[1]
        return len(directories)

    def add_children(self, child: SmartPath) -> None:
        self.children.append(child)

    def display(self, measures=(), name_max_length: int = 60):
        """Call the SmartPath display and add some relevant measures \
           to be printed alongside it."""
        output = SmartPath.display(self, measures, name_max_length)
        if "file_size" in measures:
            output += f"File size = {self.file_size!s} bytes".ljust(40)
        if "dir_count" in measures:
            output += f"Directory count = {self.dir_count!s}".ljust(40)
        if "file_count" in measures:
            output += f"File count = {self.file_count!s}".ljust(40)
        return output + "\n"
