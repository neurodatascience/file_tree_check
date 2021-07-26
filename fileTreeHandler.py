# -*- coding: utf-8 -*-
from pathlib import Path
import os
from file_tree import FileTree
import pandas as pd


class FileTreeHandler(object):
    """Docstring here"""

    def __init__(self, template, top_level):
        self.template = Path(template)
        self.top_level = Path(top_level)
        self.tree = self.read_tree_template()

    def read_tree_template(self):
        file_tree = FileTree.read(str(self.template), top_level=str(self.top_level))

        # For debug
        print(file_tree.to_string())

        return file_tree

    def update(self, common_key):
        return self.tree.update_glob(common_key, inplace=True)

    def get(self, key):
        return self.tree.get(key=str(key))
