from __future__ import annotations

import re
from abc import ABC
from abc import abstractmethod
from pathlib import Path

from file_tree import FileTree
from file_tree import Template
from file_tree.template import Literal


class SmartPath(ABC):
    """A SmartPath object is tied to a singular path (file or directory) \
    and allows itself to be printed in a readable format and allow retrieval of some statistics.

    Each instance stores their parent directory and their depth relative to the first path.

    This is an abstract class for both files and directory Paths.

    Attributes
    ----------
    path: pathlib.Path
        The path to the file/directory in question.

    parent: SmartPath or None
        Reference to the parent SmartPath. Used to determine this path's depth recursively.

    is_last: bool
        Whether or not this path is the last one to be displayed in his directory.
        Used to create the tree-like output.

    depth: int
        The path's depth in the file structure relative to the initial target directory.

    Credit to stack overflow abstrus for the visual part
    """

    # The separators for the visual representation of the file structure
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "

    def __init__(
        self,
        path: Path,
        parent_smart_path: SmartPath | None,
        is_last: bool,
        file_tree: FileTree | None = None,
    ):
        self.path = Path(str(path))
        self.parent = parent_smart_path
        self.is_last = is_last
        self.depth: int = self.parent.depth + 1 if self.parent else 0
        self.identifier: str = self.get_identifier(
            self.path,
            self.parent,
            file_tree,
        )

    def get_identifier(
        self, path: Path, parent_smart_path: SmartPath | None, file_tree: FileTree | None
    ) -> str:
        if file_tree is None:
            return self.get_identifier_base(path)
        else:
            return self.get_identifier_tree(path, parent_smart_path, file_tree)

    def parse_string_to_regex(self, string):
        string = re.sub(r"\{.*?\}", ".+", string)
        string = re.sub(r"\[(.*?)\]", r"(?:\1)?", string)
        return string

    def get_identifier_base(
        self,
        path: str | Path,
    ) -> str:
        return "not_implemented"

    def get_identifier_tree(
        self, path: str | Path, parent: SmartPath | None, tree: FileTree | None
    ) -> str:
        if parent is not None:
            parent_identifier = parent.identifier
            try:
                parent_template = tree.get_template(parent_identifier)
                templates = self.my_children(tree, parent_template).items()
            except KeyError:
                templates = tree._templates.items()
        else:
            templates = tree._templates.items()
        span = 0
        temp_late = None
        for template in templates:
            if template[1].unique_part == "." or template[1].unique_part is None:
                continue
            regex = self.parse_string_to_regex(template[1].unique_part)
            match = re.match(regex, path.name)
            if match is not None and match[0] != "":
                if match.span()[1] > span:
                    span = match.span()[1]
                    temp_late = template
                if "/" in template[1].unique_part:
                    self.unique_config(tree, template[1])
        return temp_late[0] if temp_late is not None else path.name

    def unique_config(
        self, tree: FileTree | None, template: Template | None, path: str | Path
    ) -> dict:
        if template is not None:
            for part in template._parts.parts:
                if part is Literal:
                    continue
        return None

    def my_children(self, tree: FileTree | None, parent_template: Template | None) -> dict:
        children = {}
        for template in tree._templates.items():
            if template[1].parent == parent_template and template[0] not in children:
                children[template[0]] = template[1]
        return children

    def add_stats(self, stat_dict: dict, identifier: str, measures: list[str] = []) -> dict:
        """For each measure desired adds the value from this path to the dictionary.

        Parameters
        ----------
        stat_dict: dict
        The dictionary containing the the values for each measures.

        stat_dict contains nested dictionaries with the following structure:

        .. code-block:: python

            stat_dict={
                'measure1':
                    {'identifier1': {
                        'path1': value, 'path2': value, ...},
                    'identifier2': {
                        'path3': value, 'path4': value}, ...},
                    }
                'measure2':
                    {'identifier1': {}, 'identifier2': {}, ...}
                }

        identifier: string
            The path's identifier.
            Used to aggregate this path's values to the correct place in order to add it
            with files/directories with the same identifier across the repeating file structure.

        measures: list of string
            The name of the measures to be used in the outputs.
            Each corresponds to a dictionary nested in stat_dict.

        Returns
        -------
        dict
            The same dictionary that was given but with the path's values added in.
        """
        for measure in measures:
            if identifier not in stat_dict[measure]:
                stat_dict[measure][identifier] = {}

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
    def file_size(self) -> int:
        return int(self.path.stat().st_size)

    @property
    def modified_time(self) -> int:
        return int(self.path.stat().st_mtime)

    @abstractmethod
    def file_count(self):
        raise NotImplementedError()

    @abstractmethod
    def dir_count(self):
        raise NotImplementedError()

    def display(self, measures=(), name_max_length: int = 60) -> str:
        """Return the name of the file/folder with whitespaces to fit the standard length.

        Parameters
        ----------
        measures: list of string
        name_max_length: int

        Returns
        -------
        string
        """
        return str(self.path.name).ljust(name_max_length - self.depth * 3)

    def displayable(self, measures=(), name_max_length: int = 60) -> str:
        """Return a string corresponding to a single line \
           in the file structure tree visualisation."""
        # If the path is the root, no separators are needed at the beginning of the line
        if self.parent is None:
            return self.display(measures, name_max_length)

        # If the path is the last in it's directory,
        # it will begin with └── instead of ├──"
        _filename_prefix = (
            self.display_filename_prefix_last
            if self.is_last
            else self.display_filename_prefix_middle
        )

        # Display the info about the file/directory after the prefix chose above
        parts = [f"{_filename_prefix!s} {self.display(measures, name_max_length)!s}"]

        # Now that the display for the current directory is ready, we need to add
        # the separator for each target_depth level
        parent = self.parent
        # Going up the parent hierarchy
        while parent and parent.parent is not None:
            # If the parent was last in it's directory,
            # the separator is '   ' otherwise it is '│   '
            parts.append(
                self.display_parent_prefix_middle
                if parent.is_last
                else self.display_parent_prefix_last
            )
            parent = parent.parent

        # Putting it all together in a single string
        return "".join(reversed(parts))
