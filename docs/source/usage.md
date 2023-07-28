# Usage

There are two ways to use file_tree_check. It can either be installed and used as a CLI tool
or you can fork the repository and use it as a python script. The instructions for each are
different, but the underlying principles are the same.

## Inputs

There are two things that always must be inputted into the program, the root directory, and a File_Tree template. There are a couple ways to pass this information which will be elaborated on later.
Optionally you can also input a config file that the program will read for your configuration options.

### Root Directory

This is the directory where your tree is rooted. The contents of this directory are what will be analyzed.

### File_Tree template

This is how you template for the program what you expect the structure of the dataset to be. This will be described in detail in its own section of the documentation.

### Config file

This is an optional input that streamlines the process of configuring parameters individually. The options are explained in detail under Usage as Python script/Configure config file.

## Outputs

There are several output options you will see but at the moment only two are recommended for use. Unless specified otherwise all outputs will be deposited in a folder called 'results' in your current working directory.
The primary output is a summary.txt file. The specifics of this file can vary depending on your configuration.
The other output you may find useful is the Tree. This is a visual output of the tree structure itself. This can be useful for ensuring that tree discovery is executed as intended.

## Usage as CLI

### Installation as CLI

```
git clone https://github.com/neurodatascience/file_tree_check.git
cd file_tree_check
pip install .
```

### Usage as CLI

To run with default settings, use the following command:
```
file_tree_check -r {root directory} -f {file_tree}
```
When inputting file_tree you can either input a path to a file_tree or you can use the short name* of one of the built in file_trees**.
Ex:
```
file_tree_check -r {root directory} -f bids_raw
```
*The short name is just the name of the file_tree without the '.tree' extension.
**Current built in trees are bids_raw, fMRIPrep, and freesurfer. More are on the way, if you require another feel free to open an issue on the github repository requesting one.

### Commands

`-c` or `--config`: Specifies the path to the configuration file. Usage: `-c path/to/configfile`

`-r` or `--root`: Specifies the path to the root directory to be explored. Usage: `-r path/to/root/directory`

`-f` or `--file_tree`: Specifies the path to the file tree to be used. Usage: `-f path/to/file/tree` or `-f name_of_std_file_tree`

`-ff` or `--filter_files`: If this flag is present, files will be filtered. Usage: `-ff`

`-fd` or `--filter_directories`: If this flag is present, directories will be filtered. Usage:
`-fd`

`-fh` or `--filter_hidden`: If this flag is present, hidden files and directories will be filtered. Usage: `-fh`

`-fc` or `--filter_custom`: Specifies a list of files and directories to be ignored by the program. Usage: `-fc name1,name2,...`

`-mfc` or `--file_count`: If this flag is present, the file_count measure will be on. Usage: `-mfc`

`-mdc` or `--dir_count`: If this flag is present, the dir_count measure will be on. Usage: `-mdc`

`-ms` or `--file_size`: If this flag is present, the file_size measure will be on. Usage: `-ms`

`-mt` or `--modified_time`: If this flag is present, the modified_time measure will be on. Usage: `-mt`

`-mtr` or `--time_round`: Specifies the rounding margin for modified time measurement (in seconds). Default is 500 seconds Usage: `-mtr integer_value`

`-msr` or `--size_rounding`: Specifies the rounding percentage for file size measurement. Based off of percentage of mean. Default is .01 Usage: `-msr float_value`

`-o` or `--output`: Specifies the path to the output directory. Relevant output files will be overwritten/created. Usage: `-o path/to/output/directory`

`-os` or `--summary`: If this flag is present, a summary file will be created. Usage: `-os`

`-ot` or `--tree`: If this flag is present, a text tree file will be created. Usage: `-ot`

`-oc` or `--csv`: If this flag is present, a csv file will be created. Usage: `-oc`

`-p` or `--pipe_data`: If this flag is present, data will be piped to stdout. Usage: `-p`

`-gc` or `---get_configurations`: If this flag is present, directory content configurations
will be compared. Usage: `-gc`

`-td` or `--target_depth`: Specifies the target depth for directory content configurations. Usage: `-td integer_value`

`-dr` or `--depth_range`: Specifies a range of depths for directory content configurations. Usage: `-dr integer_value1 integer_value2`.

`-dl` or `--depth_limit`: Specifies the depth limit of exploration. Usage: `-dl integer_value`

`-l` or `--log`: Specify a path to log file. Usage: `-l path\to\logfile`

`-ll` or `--loge_level`: Specify log level. Usage: `-ll DEBUG`

`-v` or `--verbose`: If toggled then verbose mode will be on. Usage: `-v`

`-d` or `--debug`: If toggled then debug mode will be on. Usage: `-d`

## Usage as Python script

You can also use file_tree_check as a python script. This may be more convenient if you prefer using custom config file to specify parameters.

### Installation as Python script

#### Clone the repository

First fork the repository to allow to save your modifications of the config file
on github, then clone the forked repository on your machine.

You can then run the following command in a terminal to install the package and
its dependencies.

```bash
pip install .
```

### Configure config file

Inside the _src/file_tree_check_ folder in your local installation, open the
`src/file_tree_check/config.ini` file and change the options to suit your need
and use case.

Be sure to modify the paths to the proper locations you want the outputs to be
saved in. By default root directory and file tree paths are left empty. This will return an error unless you pass these arguments through the command line, so it is recommended to configure these to your use.

By default the config.ini file in file_tree_check folder will be used. To change this edit line ~17 of main.py to add path to another config.ini file.

The config options are detailed in the
["Config File" section of the documentation](https://file-tree-check.readthedocs.io/en/latest/config.html).

### Running the script

Once the repository and config files are set up running the script is fairly simple. From the command line, run python and give it the main.py path to launch the script. Remember that file_tree_check requires a root directory and a file_tree. If you haven't configured these paths in the config.ini file pass them as arguments.
Example with root directory and file_tree paths in config file:
```
python main.py
```
Example with root directory and file_tree paths passed as arguments:
```
python main.py -r {root directory} -f {file_tree}
```
Notes:
-Depending on your operating system to run a python script you may type python or py3.
-To run main.py make sure you're calling it with the correct relative path. (if cwd is not file_tree_check)
-The same options apply for passing file_tree as in [Usage as CLI](#usage-as-cli-1) section.
