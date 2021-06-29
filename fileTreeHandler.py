# -*- coding: utf-8 -*-
from pathlib import Path
import os
import file_tree
import pandas as pd
import argparse


def read_tree_template(path):
    dataset_tree = file_tree.FileTree.read(str(path), dataset=path.name)





def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    pars.add_argument('start_location', type=str, help="Directory to explore")

    return pars

