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

## Structure of the script

- **_main.py_** is where the sequential series of processing takes places.

- **_statBuilder.py_** handles the creation of the output files.

- **_identifierEngine.py_** contains the IdentifierEngine class. This class is
  used to extract the identifier string from files and directories based on the
  regular expression given to it (from the config file).

- **_smartPath.py_** contains the SmartPath abstract class. The SmartFilePath
  and SmartDirectoryPath both inherit from it.

- **_smartFilePath.py_** contains the SmartDirectoryPath class, the
  implementation of SmartPath for files.

- **_smartDirectoryPath.py_** contains the SmartFilePath class, the
  implementation of SmartPath for directories.

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

## Potential improvement to the script

### Create clearer plots

Not much is done in statBuilder.create_plots() to make the image look better and
clear when a lot of plots are shown at once.

### Apply rounding in measures of file size and modification time

Presently, having a 1 byte difference in size or a difference of 1 second in
time of last modification is enough for files and directories to be flagged as
different and potential outlier. Rounding these values or using thresholds would
make for more relevant comparisons. However, this threshold or rounding factor
should ideally be modifiable by the user.

### Avoid creating a new object for each file/directory

The creation and usage of SmartPath objects takes time and memory that is not
insignificant for large dataset. Using pathlib.Path or simply iterating once
with os.walk() and getting every single operation and metrics at once might
yield significant improvements in performance but would require a major rewrite
and could be challenging to keep readable and maintanable.

### Create a branch of the script without the plot generation for easier installation

Currently, the only functions that necessitate the 3.6+ python and the required
libraries are the plot generation. Having a branch without the plot functions
would allow the script to run without installing any libraries and with a python
version potentially down to 3.2 (when argparse was introduced).
