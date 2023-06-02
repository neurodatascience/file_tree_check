# file_tree_check

File checking project for McGill NeuroDataScience - ORIGAMI lab

The file_tree_check package takes a repeating file organization (large amount of
folders with same name or files with similar name) and will do comparisons
between every occurrences to highlight missing or unusual files/folders.

Written initially for neural imaging data structure like
[BIDS](https://bids.neuroimaging.io/) but compatible with any data structure
where folder names and file of similar name are repeating (a regular expression
is used to remove any non-repeating part if needed).

---

## Installation

### Requirements

Requires python >=3.8.

The required python libraries are the following are listed in the
[pyproject.toml](pyproject.toml) file.

### Clone the repository

First fork the repository to allow to save your modifications of the config file
on github, then clone the forked repository on your machine.

You can then run the following command in a terminal to install the package and
its dependencies.

```bash
pip install .
```

### Modify the config file for your need

Inside the _src/file_tree_check_ folder in your local installation, open the
`src/file_tree_check/config.ini` file and change the options to suit your need
and use case.

Be sure to modify the paths to the proper locations you want the outputs to be
saved in.

The config options are detailed in the
["Config File" section of the documentation](https://file-tree-check.readthedocs.io/en/latest/config.html).

### Enter your config file path at line ~19 of main.py

For the script to locate your config file no matter from where the script is
run, the absolute path to the config file should be given at the top of the
`src/file_tree_check/main.py`.

## Usage

### Overview

Given a directory, will explore recursively every directory and file under it
while taking some measures for each (e.g. file size, time of modification, how
many files in the directory, etc...).

Then, it will output a comparison between folders and files with similar name,
in the form of plot distribution, a summary text file, a visualization of the
file tree or/and a csv file containing every point of measure taken.

This information can be used to find outliers and problematic files in a
directory were a regular structure in term of file count and file size is
expected.

### Running the script

Once the repository and the config files are set up, using the script is fairly
simple. From the command line, run python and give it the main.py path to launch
the script and add the target's folder path as argument.

```bash
python main.py <target_folder>
```

This will run the file checking script with the target folder as root and create
the outputs requested in the config file. Note that if the script is run from
outside `src/file_tree_check`, don't forget to include the actual path to the
`main.py` file instead.
