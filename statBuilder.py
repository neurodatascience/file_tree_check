import pandas as pd
import seaborn
from pathlib import Path
import file_tree

class StatBuilder():
    """
    Explore the template to create distribution and print vizualisation
    """

    def __init__(self, std_output=True):
        self.std_ouput = std_output
        self.pipelines = {}

    def add_session(self, path, tree_file):
        pd.DataFrame()

    def add_pipeline(self, name, subject, file_count=0):
        self.pipelines[name] = file_count

