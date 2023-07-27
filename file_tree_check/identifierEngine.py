from __future__ import annotations

import logging
import re
from pathlib import Path

from file_tree import FileTree
from smartPath import SmartPath


class IdentifierEngine:
    """Class that can extract an "identifier" from a path.

    The identifier is a name that is used for comparison between directories and
    should not contain any part that is unique (like a subject number).
    The regular expression in the config files are relied on
    to remove these unique parts of the file/directory name.

    Example:

    "sub-15464521_image.png" and "sub-25484441_image.png"
    would both have the same identifier "_image.png"
    if using a regular expression that is keeping everything
    after the first "_" like "/_.*$/".

    Attributes
    ----------
    file_expression: string
        The regular expression to filter the identifier from the name of files.

    directory_expression: string
        The regular expression to filter the identifier from the name of directories.

    logger: logging.Logger
        Logger to save info and debug message.
        Will send the log lines to the appropriate outputs following
        the logger configuration in main.py.
    """

    def __init__(self, file_expression: str, directory_expression: str, check_file: bool):
        self.file_expression = file_expression
        self.directory_expression = directory_expression
        self.logger = logging.getLogger(f"file_tree_check.{__name__}")
        self.logger.info("Created an instance of IdentifierEngine")
        self.check_file = check_file

    def get_identifier(
        self, path: str | Path, parent: SmartPath | None, file_tree: FileTree | None
    ) -> str:
        if file_tree is None:
            return self.get_identifier_base(path)
        else:
            return self.get_identifier_tree(path, parent, file_tree)

    def get_identifier_base(
        self, path: str | Path, prefix_file_with_parent_directory: bool = False
    ) -> str:
        """Extract the identifier from the file/directory.

        The identifier should be the repeating part of the name that ties it
        to it's type for comparison

            "sept_6_weekly_report.txt" -> "_weekly_report.txt"

        However the details of what precisely to extract and treat as an identifier is handled
        by the regular expressions given on creating the class instance.
        Since the regular expression is used with ``re.search()``, only the first match is kept.

        If no match is found, the entire file/directory name is used instead
        since we prefer to have identifier
        that are unique but can still be used in the output vs an empty identifier.

        Extraction method with the default regular expression:

        .. code-block::

            Files = "_.*$" ; Keep everything after the first "_". to remove the subject number.
            Directories = "^.*-" ; Keep everything until the first "-".

            ; This way, subject directories like "sub-012012" are all aggregated
            ; under "sub-" while directory names without "-" are kept entirely.

        Parameters
        ----------
        path: pathlib.Path or string
            The path to the file/directory for which to extract the identifier.

        prefix_file_with_parent_directory: bool, default = False
            Whether to include the parent directory as a prefix to the file's identifier.
            This is used to discriminate files that have the same name
            but are located under different subdirectories
            when filename are expected to be found at multiple places
            for each subject/configuration.

        Returns
        -------
        identifier: string
            The path's extracted identifier.
            Will be used to aggregate data on files/directories
            with the same identifier across the repeating file structure.
        """
        path = Path(path)
        if prefix_file_with_parent_directory and path.is_file():
            identifier = f"{self.get_identifier(path.parent)}/"
        else:
            identifier = ""

        if path.is_file():
            match = re.search(self.file_expression, path.name)
        elif path.is_dir():
            match = re.search(self.directory_expression, path.name)
        elif not self.check_file:
            match = re.search(self.file_expression, path.name)
        else:
            raise TypeError(f"Path is not a file nor a directory: {path}")

        # When the entire name is filtered out, we prefer using a identifier
        # that is maybe too unique over an empty one
        identifier += path.name if match is None else match.group(0)
        return identifier

    def get_identifier_tree(
        self, path: str | Path, parent: SmartPath | None, tree: FileTree
    ) -> str:
        if parent is not None:
            parent_identifier = parent.identifier
            parent_template = tree.get_template(parent_identifier)
            templates = parent_template.children(tree._templates)

        else:
            templates = tree._templates
        for template in templates:
            if template == "":
                continue
            regex = self.parse_string_to_regex(template.unique_part)
            match = re.match(regex, path.name)
            if match is not None and match[0] != "":
                return template
        return path.name

    def get_identifier_tree_old(self, path: str | Path, tree: FileTree):
        for key in tree.template_keys():
            if key == "":
                continue
            template = tree.get_template(key)
            regex = self.parse_string_to_regex(template.unique_part)
            match = re.match(regex, path.name)
            if match is not None and match[0] != "":
                return key
        return path.name

    def parse_string_to_regex(self, string):
        string = re.sub(r"\{.*?\}", ".+", string)
        string = re.sub(r"\[(.*?)\]", r"(?:\1)?", string)
        return string

    def get_identifier_template(
        self, path: str | Path, templates: list[str], prefix_file_with_parent_directory: bool = True
    ):
        for template in templates:
            if template[2] == "":
                continue
            if (
                prefix_file_with_parent_directory
                and Path(path).is_file()
                and template[1] is not None
            ):
                identifier = f"{template[1]}/{template[0]}"
            else:
                identifier = f"{template[0]}"
            regex = self.parse_string_to_regex(identifier)
            actual = (
                f"{path.parent.name}/{path.name}"
                if prefix_file_with_parent_directory and path.is_file()
                else path.name
            )
            match = re.match(regex, actual)
            if match is not None and match[0] != "":
                return template[2]
        return path.name
