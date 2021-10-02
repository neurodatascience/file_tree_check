# file_tree_check
File checking project for McGill NeuroDataScience - ORIGAMI lab

The file_tree_check package takes a repeating file organization (large amount of folders with same name or files with similar name) and will do comparisons between every occurences to highlight missing or unusual files/folders.

Written initially for neural imaging data structure like [BIDS](https://bids.neuroimaging.io/) but compatible with any data structure where folder names and file of similar name are repeating (a regular expression is used to remove any non-repeating part if needed).


## Installation

### Clone the repository

First fork the repository to allow to save your modifications of the config file on github, then clone the forked repository on your machine.

### Modify the config file for your need
Inside the *src/file_tree_check* folder in your local installation, open the *config.ini* file and change the options to suit your need and use case.

Be sure to modify the paths to the proper locations you want the outputs to be saved in.

The config options are detailed in the "Config File" section of the readme below.

### Enter your config file path at line ~19 of main.py

For the script to locate your config file no matter from where the script is run, the absolute path to the config file should be given at the top of the *main.py* file found under *src/file_tree_check*.

## Usage

### Overview

Given a directory, will explore recursively every directory and file under it while taking some measures for each (e.g. file size, time of modification, how many files in the directory, etc...).

Then, it will output a comparison between folders and files with similar name, in the form of plot distribution, a summary text file, a visualization of the file tree or/and a csv file containing every point of measure taken.

This information can be used to find outliers and problematic files in a directory were a regular structure in term of file count and file size is expected.

### Running the script

Once the repository and the config files are set up, using the script is fairly simple. From the command line, run python and give it the main.py path to launch the script and add the target's folder path as argument.

```
python3 main.py <target_folder>
```

This will run the file checking script with the target folder as root and create the outputs requested in the config file.
Note that if the script is run from outside "src/file_tree_check", don't forget to include the actual path to the "main.py" file instead.   


### Example for running in a HPC environment

### Use case examples

This section will provide config files for some common use case dependent on the analysis and the outputs necessary for each one.
In the examples of config file, sections with text between <> need to be replaced with your values or preferences (e.g. the path to the output file to be generated, whether or not to print plots to the screen).

#### 1: Get the tree-like text representation of a file structure to understand how it is organized.
If understanding the organization of your files is what you want more than any metrics, this is how to get the tree structure in a text file.

This config file produces only the tree output and sets the search criteria and categorization section with regular expression that do not exclude any file.
Any measures set to "yes" in the config will be displayed in the tree output alongside their file/directory.
Example of config file :
```
[Categorization]
regular expression for file identifier = ^.*$
regular expression for directory identifier = ^.*$

[Search Criteria]
use search criteria = no
regular expression for search criteria =
filter files = no
filter directories = no

[Measures]
file_count = yes
dir_count = no
file_size = yes
modified_time = yes

[Visualization]
create plots = no
number of plot per measure = 
print plots = 
save plots = 
image path = 

[Output]
create summary = no
summary output path = 
create text tree = yes
tree output path = <output path>
create csv = no
csv output path = 

[Configurations]
get number of unique configurations = no
target depth = 

[Logging]
file log path = <log path>
file log level = DEBUG

[Pipeline]
pipe file data = no
```

#### 2) Verify a neuroimaging dataset for anomalies.

In a neuroimaging dataset, we expect files to be strictly following a file organization (e.g. BIDS) and we want to be aware of any deviation from the common structure.

In this case, using the summary output and the [Configurations] section will find the most common configuration (here the file and folders present under each sub-xx folder).

To this end, first, it is assumed that all the subject folders are directly under the folder given to the script (depth=1).
Second, the [Categorization] section uses the regular expression "_.*$" to remove any subject number from the file identifiers (sub-123_T1.gz -> _T1.gz). 

The regular expression "^.*-" is used to remove the subject number from directories (sub-123 -> sub-).
Removing the uniques numbers means that every sub folder and every file can be compared to each other to find outliers.


```
[Categorization]
regular expression for file identifier = _.*$
regular expression for directory identifier = ^.*-

[Search Criteria]
use search criteria = no
regular expression for search criteria =
filter files = no
filter directories = no

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create plots = yes
number of plot per measure = <your value>
print plots = <yes/no>
save plots = yes
image path = <output path 1>

[Output]
create summary = yes
summary output path = <output path 2>
create text tree = no
tree output path = 
create csv = yes
csv output path = <output path 3>

[Configurations]
get number of unique configurations = yes
target depth = 1

[Logging]
file log path = <log path>
file log level = DEBUG

[Pipeline]
pipe file data = no
```

#### 3) Get data on only a specific selection of files or directories in a large file structure.

Here the search criteria is used to filter through the element inside the target directory.

Files and/or directories (depending on settings) will be discarded if they do not match the regular expression.

The search criteria is matched to the path's name itself, not any identifier created using the regular expressions of [Categorization].

Note that when filtering directories, the sub-directories and files contained within will be discarded from the search as well, regardless if those match the expression or not.

Filtering only files is useful for keeping only a specific type of file in every folder. 

Filtering only directories is useful for finding and analysing a single directory or type of directory. However, if this directory has a parent that does not match the regular expression, it will be discarded along with its parent before being found.
Therefore these folders should be contained directly under the directory on which the script is run.

```
[Categorization]
regular expression for file identifier = ^.*$
regular expression for directory identifier = ^.*$

[Search Criteria]
use search criteria = yes
regular expression for search criteria = <your regular expression>
filter files = <yes/no>
filter directories = <yes/no>

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create plots = no
number of plot per measure = 
print plots = 
save plots = no
image path =

[Output]
create summary = yes
summary output path = <output path 2>
create text tree = no
tree output path = 
create csv = yes
csv output path = <output path 3>

[Configurations]
get number of unique configurations = no
target depth = 1

[Logging]
file log path = <log path>
file log level = DEBUG

[Pipeline]
pipe file data = no
```


#### 4) Run an automated test on specific type of files contained in a large dataset

With the *pipe file data* setting, the script will print to the standard output a string for every file as it goes along exploring the file structure in the target folder.

This string contains the path, along with some metrics, and can be then used as input for a automated test on the file using the path in the string.

The string output for each file will have this format : 'absolute_path,identifier,file_size,modified_time' 

Combining the search criteria and this string output, the script will only output a string for every file whose name match the criteria. For example, if a test needs to be run only on json files, a search criteria that matched files ending with ".json" will have the script generate a string for every json file that can be piped to an automated test script.

This config file will also create a csv that can be uses by other type of tests.

```
[Categorization]
regular expression for file identifier = ^.*$
regular expression for directory identifier = ^.*$

[Search Criteria]
use search criteria = yes
regular expression for search criteria = <your regular expression>
filter files = yes
filter directories = no

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create plots = no
number of plot per measure = 
print plots = 
save plots = no
image path =

[Output]
create summary = no
summary output path = 
create text tree = no
tree output path = 
create csv = yes
csv output path = <output path>

[Configurations]
get number of unique configurations = no
target depth = 1

[Logging]
file log path = <log path>
file log level = DEBUG

[Pipeline]
pipe file data = yes
```


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
In a repeating file structure, we need to aggregate files and directories that are equivalent to each other under a common name.
This name is the identifier and can be simply the name of the file or directory or is extracted from its name with a regular expression to only keep the par of the name that is coming to every equivalent file.

Example: the directories "sub-15056", "sub-15888", "sub-24530", etc. would be aggregated under the identifier "sub-" for the regular expression "^.*-". This identifier will then be used to compare them between each other.

Files their parent folder as a prefix in their identifier to allow a distinction between files of the same name but in different locations under the same "subject" folder.

#### Configuration

A unique layout of files and sub-directories. In this script, two directories are said to share the same configuration if they have sub-directories and files in the same arrangement with the same identifiers.

In this example, none of the folders share the same configuration :
```
folder
├── text.txt
└── image.png
folder
├── text.txt
└── imagege.png
folder
├── text.docx
└── image.png
folder
├── sub
│   └── text.txt
└── image.png
folder
└── image.png
```
*Assuming the identifiers used are the file/directory name as per default.

#### Path
A reference to a location in a directory system. All paths in this script are assumed to be absolute paths (starting from the root of the directory system) but since the paths are handled by pathlib.Path objects, relative paths should work as well.

#### SmartPath
The custom class used by this script to represent each path (file or directory). This custom class contains some methods that facilitate the computing of metrics and comparison.

#### Parent
The logical parent of the path, meaning the directory containing the path.

#### Children
The files and sub-directories contained in the directory.

#### File Structure / file hierarchy

The logical organization of the files and sub-directories under the given directory. 

#### File/directory Name
From the patlib library : "A string representing the final path component, excluding the drive and root, if any: "
```
PurePosixPath('my/library/setup.py').name
---> 'setup.py' 
```

## Structure of the script

* ***main.py*** is where the sequential series of processing takes places.

* ***statBuilder.py*** handles the creation of the output files. 

* ***identifierEngine.py*** contains the IdentifierEngine class. This class is used to extract the identifier string from files and directories based on the regular expression given to it (from the config file).

* ***smartPath.py*** contains the SmartPath abstract class. 
The SmartFilePath and SmartDirectoryPath both inherit from it.

* ***smartFilePath.py*** contains the SmartDirectoryPath class, the implementation of SmartPath for files.

* ***smartDirectoryPath.py*** contains the SmartFilePath class, the implementation of SmartPath for directories.



## Frequently Asked Questions (FAQ)

### When should I use this script?
Useful for:
* Gathering basic metrics on a large amount of file/folder.
* Finding missing or outlier file/folder in a repeating file structure
* Having a visual overview of a smaller amount of file
* Running another command/script on every file in a large directory

Less useful for :
* Finding problematic files in large amount of file/folder with no repeating structure
* If you are using a dataset that you know is strictly BIDS and are not searching for missing files. *pybids* would be more useful here
* Need data contained inside the files themselves instead of metadata.


### How much time does the script take to run on a large dataset (e.g. UK BioBank)?
In the tests using the UK Biobank with for 45 000 subject with around 20 files each (total of 860 000 files), the script
took 12 minutes to run using a Intel Gold 6148 Skylake @ 2.4 GHz and less than 900 MB of memory. (Average after 3 tests)

### The script execution seems to be stuck after a few steps
It is likely that the script is not stuck but is busy in the exploration phase where it will index and create SmartPath
objects for each file and directory present inside the root folder. For large dataset, this step can take several minutes.
If you are logging at the DEBUG level, to the console or to the log file, the last line before this step is "Launching exploration of the target folder".

## Potential improvement to the script

### Create clearer plots
Not much is done in statBuilder.create_plots() to make the image look better and clear when a lot of plots are shown at once.

### Apply rounding in measures of file size and modification time
Presently, having a 1 byte difference in size or a difference of 1 second in time of last modification is enough for files and directories to be flagged as different and potential outlier.
Rounding these values or using thresholds would make for more relevant comparisons.
However, this threshold or rounding factor should ideally be modifiable by the user.

### Avoid creating a new object for each file/directory
The creation and usage of SmartPath objects takes time and memory that is not insignificant for large dataset.
Using pathlib.Path or simply iterating once with os.walk() and getting every single operation and metrics at once might yield significant improvements in performance but would require a major rewrite and could be challenging to keep readable and maintanable.

