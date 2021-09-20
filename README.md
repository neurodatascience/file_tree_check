# file_tree_check
File checking project for McGill NeuroDataScience - ORIGAMI lab

The file_tree_check package takes a repeating file organization (large amount of folders with same name or files with similar name) and will do comparisons between every occurences to highlight missing or unusual files/folders.

Written initially for neural imaging data structure like [BIDS](https://bids.neuroimaging.io/) but compatible with any data structure where folder names and file of similar name are repeating (a regular expression is used to remove any non-repeating part if needed).


## Installation

### Clone the repository

### Modify the config file for your need

### Enter your config file path at line ~19 of main.py

## Usage

### Overview

Given a directory, will explore recursively every directory and file under it while taking some measures for each (e.g. file size, time of modification, how many files in the directory, etc...).

Then, it will output a comparison between folder and files with similar name, in the form of plot distribution, a summary text file, a visualization of the file tree or/and a csv file containing every point of measure taken.

This information can be used to find outliers and problematic files in a directory were a regular structure in term of file count and file size is expected.

### Simple example

```
python3 main.py <target_folder>
```

### Example for running in a HPC environnement

### Use cases
#### 1) Get the tree-like text representation of a file structure to understand how it is organized.


#### 2) Verify a neuroimaging dataset for anomalies.


#### 3) Get data on only a specific selection of file or directory in a large file structure.

#### 4) Run a automated test on the files contained in 

## Config file

Modifying the config file is the way to tell the program what you are looking for, what outputs do you want and what thoses outputs should contain.
This section will explain how to modify it and what does every command is used for.

### How to edit a config.ini file

An .ini file is simply a text file with a few rules to allow it to be readable by the parsing function. 
stuff
More information on the syntax of config file and how they are read by the configparser python library can be found [here](https://docs.python.org/3/library/configparser.html) 


### Options Breakdown


## Glossary

Short explanation of some terms used in the documentation and the code.

#### Identifier

#### Configuration

#### Path

#### SmartPath

#### Parent

#### Children

#### File Structure

## Structure of the script



## Frequently Asked Questions (FAQ)

### When should I use this script?

### How much time does the script take to run on a large dataset (e.g. UK BioBank)?
In the tests using the UK Biobank with for 45 000 subject with around 20 files each (total of 860 000 files), the script
took 12 minutes to run using a Intel Gold 6148 Skylake @ 2.4 GHz and less than 900 MB of memory. (Average after 3 tests)

### The script execution seems to be stuck after a few steps.
It is likely that the script is not stuck but is busy in the exploration phase where it will index and create SmartPath
objects for each file and directory present inside the root folder. For large dataset, this step can take several minutes.
If you are logging at the DEBUG level, to the console or to the log file, the last line before this step is "Launching exploration of the target folder".
If this is not the case or if this 


