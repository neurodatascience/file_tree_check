# FAQ

### How do I install this script?

Simply clone the github repository found [here] with for example:
`git clone https://github.com/neurodatascience/file_tree_check.git` to install
it under your current directory. Once cloned, you only need to customize the
config file to your need and run the "main.py" file and passing the target
directory in argument.

### When should I use this script?

Useful for:

- Gathering basic metrics on a large amount of file/folder.
- Finding missing or outlier file/folder in a repeating file structure
- Having a visual overview of a smaller amount of file
- Running another command/script on every file in a large directory

Less useful for :

- Finding problematic files in large amount of file/folder with no repeating
  structure
- If you are using a dataset that you know is strictly BIDS and are not
  searching for missing files. _pybids_ would be more useful here
- Need data contained inside the files themselves instead of metadata.

### How much time does the script take to run on a large dataset (e.g. UK BioBank)?

In the tests using the UK Biobank with for 45 000 subject with around 20 files
each (total of 860 000 files), the script took 12 minutes to run using a Intel
Gold 6148 Skylake @ 2.4 GHz and less than 900 MB of memory. (Average after 3
tests)

### The script execution seems to be stuck after a few steps

It is likely that the script is not stuck but is busy in the exploration phase
where it will index and create SmartPath objects for each file and directory
present inside the root folder. For large dataset, this step can take several
minutes. If you are logging at the DEBUG level, to the console or to the log
file, the last line before this step is "Launching exploration of the target
folder".
