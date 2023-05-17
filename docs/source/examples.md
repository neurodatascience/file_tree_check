# Examples

This section will provide config files for some common use case dependent on the
analysis and the outputs necessary for each one. In the examples of config file,
sections with text between <> need to be replaced with your values or
preferences (e.g. the path to the output file to be generated, whether or not to
print plots to the screen).

## Get the tree-like text representation of a file structure to understand how it is organized.

If understanding the organization of your files is what you want more than any
metrics, this is how to get the tree structure in a text file.

This config file produces only the tree output and sets the search criteria and
categorization section with regular expression that do not exclude any file. Any
measures set to "yes" in the config will be displayed in the tree output
alongside their file/directory. Example of config file :

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

## Run an automated test on specific type of files contained in a large dataset

With the _pipe file data_ setting, the script will print to the standard output
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
