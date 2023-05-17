# The Config File

Modifying the config file is the way to tell the program what you are looking
for, what outputs do you want and what those outputs should contain. This
section will explain how to modify it and what does every command is used for.

## How to edit a config.ini file

An .ini file is simply a text file with a few rules to allow it to be readable
by the parsing function. stuff More information on the syntax of config file and
how they are read by the configparser python library can be found
[here](https://docs.python.org/3/library/configparser.html)

### Config Options Breakdown

This section will provide explanation for each option in the config file. The
.ini structure is quite flexible and easy to read but here is some important
fact to know :

- Boolean values can be "true", "false" or "yes", "no" or a mix of the two
  without creating any trouble.
- In most sections, a bool option will enable the functionality that will then
  import the following option it needs. This means that when desactivating a
  feature by setting the bool to false the relevant following options can be
  ignored and left empty.
- Not putting any values after the "=" will produce an empty string as the
  value.
- The type mentioned here for each option is how the script will import and
  interpret the value. This means for example that an option that is expecting
  an int will raise an error if you write letters in the value.

**[Categorization]**

regular expression for file identifier = string

    The regular expression to filter the identifier from the name of files. Will be used to re.search() on any file's name. The first match found will be kep as identifier

regular expression for directory identifier = string

    The regular expression to filter the identifier from the name of directories.

**[Search Criteria]**

use search criteria = bool

    Whether or not to filter files and/or directory to extract data and metrics from only the subset that match the regular expressions below.

regular expression for search criteria = string

    A regular expression to be used to filter files and/or directories included in the analysis. Uses re.match() to filter with the regular expression.

filter files = bool

    Whether or not the search criteria will be used to discard files whose names do not match the regular expression.

filter directories = bool

    Whether or not the search criteria will be used to discard directories whose names do not match.

**[Measures]**

file_count = bool

    Take or not the measure of the number of files present in each directory (does not include files in sub-directories).

dir_count = bool

    Take or not the measure of the number of sub-directories present in each directory (does not include directories nested inside those sub-directories).

file_size = bool

    Take or not the measure of the size of the file/directory in bytes.

modified_time = bool

    Take or not the measure of the time of last modification, in seconds since 1st January 1970 (epoch time).

**[Visualization]**

create plots = bool

    Whether or not to create the plots that will show the distribution of the collected metrics between files and directories with the same identifier

number of plot per measure = int

    How many identifiers will be included in the plots, starting from the ones with the highest number of occurrences.
    Corresponds to the number of column of the plot figure, it's rows being dictated by the number of measures taken.

print plots = bool

    Whether to show or not the plots with matplotlib.pyplot.show() before exiting the function.

save plots = bool

    Whether or not to save the plots generated as a image file.

image path = string

    The path to where the graphs should be saved. If not given or None, will not save the plots as file.

**[Output]**

create summary = bool

    Whether or not to create the text summary file that will highlights common file configurations if requested and will point to outliers for each measure and file/directory type.

summary output path = string

    The path to where the text summary file should be saved.

create text tree = bool

    Whether or not to create the tree-like file structure visualization in a text file.

tree output path = string

    The path to the text file where the file tree output will be saved. If none, the type of output is skipped.

create csv = bool

    Whether or not to create the csv file containing a row for each file and directory found along with the metrics for each.

csv output path = string

    Path to where the CSV should be saved.

**[Configurations]**

get number of unique configurations = bool

    Whether or not to compare the configuration of the folders in the repeating structure.

target depth = int

    Specify which depth of folder to use for configuration comparison. (e.g. if comparing each sub folders found directly under the target folder given to the script, depth=1)

**[Logging]**

file log path = string

    The path to the file where to save the logs. If is None, will not save path to any files.

file log level = string

    The level of logging for the log file. Either "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" or "NOTSET".

**[Pipeline]**

pipe file data = bool

    Whether to output the data from each file found directly to the standard output during the execution. By default this will print in the console which is not recommended for large dataset.
    If the script is followed by a pipe, this will pass the data to the other script or command. Only outputs files because directories shouldn't be relevant for the custom tests.
    Outputted format is  a single string per file in the format : 'path,identifier,file_size,modified_time'. File_size is in bytes, modified_time is in seconds (epoch time).
