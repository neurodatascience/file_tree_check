import re
from pathlib import Path
import logging


class IdentifierEngine:
    """
    Class that can extract an "identifier" from a path. This is a name that is used for comparison between folders and
    should not contain any part that are unique to all others (like a subject number). The regular expression in
    the config files are relied on to remove these unique parts of the file/folder name.
    """
    def __init__(self, file_expression, folder_expression):
        self.file_expression = file_expression
        self.folder_expression = folder_expression
        self.logger = logging.getLogger("file_tree_check.{}".format(__name__))
        self.logger.info("Created an instance of IdentifierEngine")

    def get_identifier(self, path, prefix_file_with_parent_folder=True):
        """
        Files : We identify file type by removing the subject number, which is the text before the first "_"
        and adding the parent folder name in front.
        Folders : The folder name ("anat", "sub-..") is directly used for comparison.
        """
        path = Path(path)
        if prefix_file_with_parent_folder and path.is_file():
            identifier = self.get_identifier(path.parent) + "/"
        else:
            identifier = ""

        if path.is_file():
            match = re.search(self.file_expression, path.name)
        elif path.is_dir():
            match = re.search(self.folder_expression, path.name)
        else:
            raise TypeError("Path is not a file nor a folder : {}".format(path))
        # When the entire name is filtered out, we prefer using a identifier that is maybe too unique over an empty one
        if match is None:
            identifier += path.name
        else:
            identifier += match.group(0)
        return identifier