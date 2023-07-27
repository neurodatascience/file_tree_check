# Configuration

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

#### Categorization

##### regular_expression_file_identifier = string

The regular expression to filter the identifier from the name of files. Will be
used to re.search() on any file's name. The first match found will be kep as
identifier. (deprecated)

##### regular_expression_directory_identifier = string

The regular expression to filter the identifier from the name of directories.
(deprecated)

#### Search Criteria (search criteria use is not recommended at this time)

##### use_search_criteria = bool

Whether or not to filter_files and/or directory to extract data and metrics from
only the subset that match the regular expressions below.

##### regular_expression_search_criteria = string

A regular expression to be used to filter_files and/or directories included in
the analysis. Uses re.match() to filter with the regular expression.

#### Filter

##### filter_files = bool

Whether or not the search criteria will be used to discard files whose names do
not match the regular expression.

##### filter_directories = bool

Whether or not the search criteria will be used to discard directories whose
names do not match.

##### filter_hidden = bool

Whether or not to discard hidden files. These are files that begin with a '.'.
Turned on by default.

##### filter_custom = bool

Whether or not to use a custom list to discard specific files and directories.
Must be used in conjunction with filter_custom_list.

##### filter_custom_list = string

List of file and directories names for program to ignore. Deliniate the names with
commas ','. White spaces will be trimmed.
Ex: code,logs,sourcedata or code, logs, sourcedata


#### Measures

##### file_count = bool

Take or not the measure of the number of files present in each directory (does
not include files in sub-directories).

##### dir_count = bool

Take or not the measure of the number of sub-directories present in each
directory (does not include directories nested inside those sub-directories).

##### file_size = bool

Take or not the measure of the size of the file/directory in bytes. If using
this measure it is highly recommended to use size_rounding_percentage.

##### modified_time = bool

Take or not the measure of the time of last modification, in seconds since 1st
January 1970 (epoch time). If using this recommended to use time_rounding_seconds
as well.

#### Measures.Averaging

##### time_rounding_seconds = integer

For each file type determined by the program the mean modified time is calculated.
This parameter will round all files within the specified number of seconds from the
mean.

##### size_rounding_percentage = float

For each file type determined by the program the mean size is calculated.
This parameter specifies what percent of deviation from the mean to round to.
If parameter is set to .01 then a percentage of 1% is used.

#### Output

##### create_summary = bool

Whether or not to create the text summary file that will highlights common file
configurations if requested and will point to outliers/norm for each measure and
file/directory type.

##### summary_output_path = string

The path to where the text summary file should be saved. By default is saved
to a directory called results in current working directory.

##### create_text_tree = bool

Whether or not to create the tree-like file structure visualization in a text
file.

##### tree_output_path = string

The path to the text file where the file tree output will be saved. If none, the
type of output is skipped. By default is saved to a directory called results
in current working directory.

##### create_csv = bool

Whether or not to create the csv file containing a row for each file and
directory found along with the metrics for each.

##### csv_output_path = string

Path to where the CSV should be saved. By default is saved
to a directory called results in current working directory.

#### Output.Visualization
Use is not recommended at this time.
##### create_plots = bool

Whether or not to create the plots that will show the distribution of the
collected metrics between files and directories with the same identifier

##### number_plot_per_measure = int

How many identifiers will be included in the plots, starting from the ones with
the highest number of occurrences. Corresponds to the number of column of the
plot figure, it's rows being dictated by the number of measures taken.

##### print_plots = bool

Whether to show or not the plots with matplotlib.pyplot.show() before exiting
the function.

##### save_plots = bool

Whether or not to save the plots generated as a image file.

##### image_path = string

The path to where the graphs should be saved. If not given or None, will not
save the plots as file.

#### Output.Piping

##### pipe_data = bool
Whether to output the data from each file found directly to the standard output
during the execution. By default this will print in the console which is not
recommended for large dataset. If the script is followed by a pipe, this will
pass the data to the other script or command. Only outputs files because
directories shouldn't be relevant for the custom tests. Outputted format is a
single string per file in the format :
'path,identifier,file_size,modified_time'. File_size is in bytes, modified_time
is in seconds (epoch time).

#### Configurations

##### get_configurations = bool

Whether or not to compare the configuration of the folders in the repeating
structure. Will display in summary the different configurations for a
directory type. The configuration is a list of the directories and files
within the directory.

##### target_depth = int

Specify which depth of folder to use for configuration comparison. Useful if
you only want to compare one level. (e.g. if comparing each sub folders found
directly under the target folder given to the script, depth=1)

##### use_depth_range = bool

Whether or not to specify a range of depths to compare configurations.
Must be used in conjunction with range_start and range_end.

##### range_start = int

The beginning of range to compare configurations. This is inclusive, so
if range_start = 0, then the root directory will be included.

##### range_end = int

The end of range to compare configurations. This is inclusive as well.

##### limit_depth = bool

Whether or not to limit depth of tree discovery. This could be useful when dealing
with very large trees and not looking at contents beyond a certain depth.

##### depth_limit = int

The specified depth limit. This is inclusive so if depth limit = 1 then
children of root directory will be found but nothing deeper than that.

#### Logging

##### log_path = string

The path to the file where to save the logs. If is None, will not save path to
any files. By default saves to results folder in current workind directory.

##### file_log_level = string

The level of logging for the log file. Either:

- "CRITICAL"
- "ERROR"
- "WARNING"
- "INFO"
- "DEBUG"
- "NOTSET"

#### Input

##### root_config = bool

Whether or not to use root path from config file.

##### root_path = Path

This is the path to the directory you would like the program to search on.

##### use_file_tree = bool

Whether or not to use file_tree. By default is yes, because program depends
on file_tree usage.

##### file_tree_path = Path

Path to file_tree to be used.
