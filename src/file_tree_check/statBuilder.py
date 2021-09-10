import csv
import logging
from collections import Counter
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path
import time

# Modify for a different figure size, (width, height)
FIG_SIZE = (20, 12)


class StatBuilder(object):
    """Store the data in a dictionary and create the output plots and files .

    Attributes
    ----------
    stat_dict : dict
        The dictionary containing the the values for each measures.
            stat_dict contains nested dictionaries with the following structure:
            stat_dict={
                'measure1' :
                    {'identifier1' : {
                        'path1' : value, 'path2' : value, ...},
                    'identifier2' : {
                        'path3' : value, 'path4' : value}, ...},
                    }
                'measure2' :
                    {'identifier1' : {}, 'identifier2' : {}, ...}
                }
    measures : list of string
        The name of the measures to be used in the outputs. Each name corresponds to a dictionary nested in stat_dict.
    logger : logging.Logger
        Logger to save info and debug message. Will send the log lines to the appropriate outputs following the logger
        configuration in main.py.
    """

    def __init__(self, stat_dict, measures=()):
        """Initialize an instance associated to the given statistics dictionary.

        Parameters
        ----------
        stat_dict : dict
            Contains the values for each measures. See above for the structure
        measures : list of string
            The list of measure name the StatBuilder instance should care about.
            Used in the functions to iterate over stat_dict in a safer way.
            Any measures in stat_dict that are not in this list will be ignored when creating the outputs.
        """
        self.stat_dict = stat_dict
        self.measures = measures
        self.logger = logging.getLogger("file_tree_check.{}".format(__name__))
        self.logger.info("Created an instance of StatBuilder")

    def create_plots(self, save_path=None, show_plot=True, plots_per_measure=8):
        """Create a comparison plot for each measure given in a single figure.
        One row of plots per measure.
        Will show the distribution for a given amount of file/directory identifier per measure.
        Will prioritize the distributions with the highest amount of data points.
            E.g. will show distributions for a directory type that was found 1000 time before directories that were
            found 500 times in the file structure since each directory contributes one data point to
            it's directory type distribution.

        Parameters
        ----------
        save_path :  pathlib.Path or string, default=None
            The path to where the graphs should be saved. If not given or None, will not save the plots as file.
        show_plot : bool, default=True
            Whether to show or not the plots with matplotlib.pyplot.show() before exiting the function.
        plots_per_measure : int
        """
        sns.set(style="darkgrid")
        self.logger.debug("Creating subplots objects")
        height = len(self.measures)
        fig, axes = plt.subplots(height, int(plots_per_measure), figsize=FIG_SIZE)
        fig.suptitle('Distribution in the file structure')
        self.logger.debug("Iterating over the measures in the data")
        for measure_index, measure_name in enumerate(self.measures):
            i = 0
            self.logger.debug("Iterating over the directories in the measure {}".format(measure_name))
            # Sort the measure dict (containing 'identifier' : {'path' : value}) for identifiers with the highest
            # amount of paths (and therefore values) first
            sorted_folders = {k: v for k, v in sorted(self.stat_dict[measure_name].items(),
                                                      key=lambda item: len(item[1]), reverse=True)}
            for identifier, paths in sorted_folders.items():
                # Do not show on plot when all values are 0 or None
                if all(value == 0 or value is None for value in paths.values()):
                    continue

                sns.histplot(paths, ax=axes[measure_index, i], bins=20)
                axes[measure_index, i].set_xlabel(measure_name, color="b")
                axes[measure_index, i].set_title(identifier, color="r")
                i += 1
                if i >= plots_per_measure:
                    self.logger.debug("Reached the maximum number of directories shown on the visualization")
                    break
        plt.tight_layout()
        self.logger.info("Plots created")

        if save_path is not None:
            self.logger.debug("Saving plot to file")
            fig.savefig(Path(save_path))
            self.logger.info("Saved plot at path {}".format(save_path))
        if show_plot:
            self.logger.debug("Displaying plots")
            plt.show()

    def create_summary(self, root, configurations):
        """Produce the 'Summary' text file output.

        This output highlights common file configurations if requested and will point to outliers for each measure and
        file/directory type.

        Parameters
        ----------
        root :  pahlib.Path
            Path to the root directory (target directory) of the file structure.
        configurations : dict
            Contains the file configurations found for each file/directory identifier with the following structure :
            configurations={
                'identifier1' :
                    [ {'structure' : ['identifier3', 'identifier4', 'identifier5'], 'paths' : ['path1', 'path2']},
                    {'structure' : ['identifier3', 'identifier5'], 'paths' : ['path4']},
                    ... ]
                'identifier2' :
                    [{'structure' : [], 'paths' : []}, ...]
                }

        Returns
        -------
        string
            The entire generated summary text as a single string, to be handled by main.py for saving or printing.
        """
        self.logger.debug("Initializing summary output")
        output = "***** Analysis of file structure at : '{}' *****" \
                 "\nCreated: {}\nTarget directory : {}\n\n".format(root.name, time.ctime(), root)

        if configurations is not None:
            for identifier, configuration_list in configurations.items():
                output += "\nConfigurations for directory **{}**:".format(identifier)
                sorted_config_list = [v for v in sorted(configuration_list,
                                                        key=lambda item: len(item["paths"]), reverse=True)]
                for i in range(len(sorted_config_list)):
                    output += "\n     Configuration #{} was found in {} directories. Contains the following : " \
                              "\n            {}".format(i+1, len(sorted_config_list[i]["paths"]),
                                                        sorted_config_list[i]["structure"])

        for measure_name in self.measures:
            self.logger.debug("Calculating most common occurrences for measure {}".format(measure_name))
            output += "\n\nOccurrences for measure  :     **{}**\n".format(measure_name)
            sorted_folders = {k: v for k, v in sorted(self.stat_dict[measure_name].items(),
                                                      key=lambda item: len(item[1]), reverse=True)}
            for folder_name, paths in sorted_folders.items():
                most_common_value, most_common_counter = 0, 0

                counter = Counter()
                for path, value in paths.items():
                    counter[value] += 1
                most_common_value = counter.most_common(1)[0][0]
                most_common_counter = counter.most_common(1)[0][1]

                if most_common_value is None:
                    continue

                output += "    In '{}' :\n        {} of {} found {} time\n".format(folder_name,
                                                                                   measure_name, most_common_value,
                                                                                   most_common_counter)
                if most_common_counter < len(paths):
                    output += "          Outliers :\n"
                    for path, value in paths.items():
                        if value != most_common_value:
                            output += "            {}  has : {}\n".format(str(path), value)
            self.logger.info("Found {} directories/files for measure {}".format(len(sorted_folders), measure_name))
        self.logger.info("Summary created with {} measures, file is {} characters long.".format(
            len(self.measures), len(output)))
        return output

    def create_csv(self, output_path):
        """Produce the CSV (comma-separated value) file output at the target path.

                As the name says, a CSV contains values separated by a comma.
                In this case, each line represent a single file/directory with it's identifier and the measures done.
                Format of each line is :
                    path,identifier,measure1,measure2,measure3,...
                Order of measures (but presence depends on config file option):
                    file_count, dir_count, file_size, modified_time
                All are integers:
                    file_count = number of files directly under given directory (ignores files inside subdirectories)
                    dir_count = number of directories directly under given directory (ignores inside subdirectories)
                    file_size = size in bytes rounded to the nearest integer
                    modified_time = time of last modification in number of seconds since 1st January 1970 (Epoch time)

                Parameters
                ----------
                output_path :  pahlib.Path or string
                    Path to where the CSV should be saved.
        """
        self.logger.debug("Opening csv file for writing at : {}".format(output_path))
        with open(output_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            headers = ['Path'] + ['Identifier'] + list(self.measures)
            csv_writer.writerow(headers)
            self.logger.info("Storing in CSV file with header : {}".format(str(headers)))
            # Supposing every file/directory is present in the first measure's dictionary (which should be the case)
            self.logger.debug("Iterating through every file/directory type to populate the CSV.")
            for file_identifier, paths in sorted(self.stat_dict[self.measures[0]].items()):
                "For every path found in the first measure, write all the measures for that path in the same row."
                for path, value in paths.items():
                    row = list()
                    for measure in self.measures:
                        row.append(self.stat_dict[measure][file_identifier][path])
                    csv_writer.writerow([path] + [file_identifier] + row)
        self.logger.info("CSV file closed. Contains {} bytes of data".format(Path(output_path).stat().st_size))