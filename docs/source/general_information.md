# file_tree_check

File checking project for McGill NeuroDataScience - ORIGAMI lab

The file_tree_check package takes a repeating file organization (large amount of
folders with same name or files with similar name) and will do comparisons
between every occurrences to highlight missing or unusual files/folders.

Written initially for neural imaging data structure like
[BIDS](https://bids.neuroimaging.io/) but compatible with any data structure
where folder names and file of similar name are repeating.

Uses a [file_tree](https://pypi.org/project/file-tree/) as a template for data structure.
This allows easy and convenient c onfiguration of the tool. With a properly written
file_tree any data structure is able to be analyzed.

## Requirements

Requires python >=3.8.

The required python libraries are the following are listed in the
[pyproject.toml](pyproject.toml) file.

## Demo
