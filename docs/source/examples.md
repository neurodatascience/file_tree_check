# Examples

This section will provide config files for some common use case dependent on the
analysis and the outputs necessary for each one. In the examples of config file,
sections with text between <> need to be replaced with your values or
preferences (e.g. the path to the output file to be generated, whether or not to
print_plots to the screen).

## Get the tree-like text representation of a file structure to understand how it is organized.

If understanding the organization of your files is what you want more than any
metrics, this is how to get the tree structure in a text file.

This config file produces only the tree output and sets the search criteria and
categorization section with regular expression that do not exclude any file. Any
measures set to "yes" in the config will be displayed in the tree output
alongside their file/directory. Example of config file :

```
[Categorization]
regular_expression_file_identifier = ^.*$
regular_expression_directory_identifier = ^.*$

[Search Criteria]
use_search_criteria = no
regular_expression_search_criteria =
filter_files = no
filter_directories = no

[Measures]
file_count = yes
dir_count = no
file_size = yes
modified_time = yes

[Visualization]
create_plots = no
number_plot_per_measure =
print_plots =
save_plots =
image_path =

[Output]
create_summary = no
summary_output_path =
create_text_tree = yes
tree_output_path = <output path>
create_csv = no
csv_output_path =

[Configurations]
get_number_unique_configurations = no
target_depth =

[Logging]
file_log_path = <log path>
file_log_level = DEBUG

[Pipeline]
pipe_file_data = no
```

## Verify a neuroimaging dataset for anomalies.

In a neuroimaging dataset, we expect files to be strictly following a file
organization (e.g. BIDS) and we want to be aware of any deviation from the
common structure.

In this case, using the summary output and the [Configurations] section will
find the most common configuration (here the file and folders present under each
sub-xx folder).

To this end, first, it is assumed that all the subject folders are directly
under the folder given to the script (depth=1). Second, the [Categorization]
section uses the regular expression "\_.\*$" to remove any subject number from
the file identifiers (sub-123_T1.gz -> \_T1.gz).

The regular expression "^.\*-" is used to remove the subject number from
directories (sub-123 -> sub-). Removing the uniques numbers means that every sub
folder and every file can be compared to each other to find outliers.

```
[Categorization]
regular_expression_file_identifier = _.*$
regular_expression_directory_identifier = ^.*-

[Search Criteria]
use_search_criteria = no
regular_expression_search_criteria =
filter_files = no
filter_directories = no

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create_plots = yes
number_plot_per_measure = <your value>
print_plots = <yes/no>
save_plots = yes
image_path = <output path 1>

[Output]
create_summary = yes
summary_output_path = <output path 2>
create_text_tree = no
tree_output_path =
create_csv = yes
csv_output_path = <output path 3>

[Configurations]
get_number_unique_configurations = yes
target_depth = 1

[Logging]
file_log_path = <log path>
file_log_level = DEBUG

[Pipeline]
pipe_file_data = no
```

## Get data on only a specific selection of files or directories in a large file structure.

Here the search criteria is used to filter through the element inside the target
directory.

Files and/or directories (depending on settings) will be discarded if they do
not match the regular expression.

The search criteria is matched to the path's name itself, not any identifier
created using the regular expressions of [Categorization].

Note that when filtering directories, the sub-directories and files contained
within will be discarded from the search as well, regardless if those match the
expression or not.

Filtering only files is useful for keeping only a specific type of file in every
folder.

Filtering only directories is useful for finding and analysing a single
directory or type of directory. However, if this directory has a parent that
does not match the regular expression, it will be discarded along with its
parent before being found. Therefore these folders should be contained directly
under the directory on which the script is run.

```
[Categorization]
regular_expression_file_identifier = ^.*$
regular_expression_directory_identifier = ^.*$

[Search Criteria]
use_search_criteria = yes
regular_expression_search_criteria = <your regular expression>
filter_files = <yes/no>
filter_directories = <yes/no>

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create_plots = no
number_plot_per_measure =
print_plots =
save_plots = no
image_path =

[Output]
create_summary = yes
summary_output_path = <output path 2>
create_text_tree = no
tree_output_path =
create_csv = yes
csv_output_path = <output path 3>

[Configurations]
get_number_unique_configurations = no
target_depth = 1

[Logging]
file_log_path = <log path>
file_log_level = DEBUG

[Pipeline]
pipe_file_data = no
```

## Run an automated test on specific type of files contained in a large dataset

With the _pipe_file_data_ setting, the script will print to the standard output
a string for every file as it goes along exploring the file structure in the
target folder.

This string contains the path, along with some metrics, and can be then used as
input for a automated test on the file using the path in the string.

The string output for each file will have this format :
'absolute_path,identifier,file_size,modified_time'

Combining the search criteria and this string output, the script will only
output a string for every file whose name match the criteria. For example, if a
test needs to be run only on json files, a search criteria that matched files
ending with ".json" will have the script generate a string for every json file
that can be piped to an automated test script.

This config file will also create a csv that can be uses by other type of tests.

```
[Categorization]
regular_expression_file_identifier = ^.*$
regular_expression_directory_identifier = ^.*$

[Search Criteria]
use_search_criteria = yes
regular_expression_search_criteria = <your regular expression>
filter_files = yes
filter_directories = no

[Measures]
file_count = yes
dir_count = yes
file_size = yes
modified_time = yes

[Visualization]
create_plots = no
number_plot_per_measure =
print_plots =
save_plots = no
image_path =

[Output]
create_summary = no
summary_output_path =
create_text_tree = no
tree_output_path =
create_csv = yes
csv_output_path = <output path>

[Configurations]
get_number_unique_configurations = no
target_depth = 1

[Logging]
file_log_path = <log path>
file_log_level = DEBUG

[Pipeline]
pipe_file_data = yes
```
