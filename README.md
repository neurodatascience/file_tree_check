# file_tree_check
File checking project for McGill NeuroDataScience - ORIGAMI lab

The file_tree_check package takes a repeating file organization (large amount of folders with same name or files with similar name) and will do comparisons between every occurences to highlight missing or unusual files/folders.

Written initially for neural imaging data structure like [BIDS](https://bids.neuroimaging.io/) but compatible with any data structure where folder names and file of similar name are repeating (a regular expression is used to remove any non-repeating part if needed).


## Installation



## Usage

### Overview

Given a directory, will explore recursively every directory and file under it while taking some measures for each (e.g. file size, time of modification, how many files in the directory, etc...).

Then, it will output a comparison between folder and files with similar name, in the form of plot distribution, a summary text file, a visualization of the file tree or/and a csv file containing every point of measure taken.

This information can be used to find outliers and problematic files in a directory were a regular structure in term of file count and file size is expected.

### Simple example

```
python3 main.py <target_folder>
```

### Config file



