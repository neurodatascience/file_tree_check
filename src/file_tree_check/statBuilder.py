import csv
import logging
from collections import Counter
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path
import time

FIG_SIZE = (20, 12)


class StatBuilder(object):
    """
    Store the data in a dictionary and create histograms of the distribution of the data for each folder.
    """

    def __init__(self, stat_dict, measures=()):
        self.stat_dict = stat_dict
        self.measures = measures
        self.logger = logging.getLogger("file_tree_check.{}".format(__name__))
        self.logger.info("Created an instance of StatBuilder")

    def create_graphs(self, save_file=None, show_graph=True, max_size=8):
        """Will create a comparison graph for each measure given in a single figure."""
        sns.set(style="darkgrid")
        self.logger.debug("Creating subplots objects")
        height = len(self.measures)
        fig, axes = plt.subplots(height, max_size, figsize=FIG_SIZE)
        fig.suptitle('Distribution in the file structure')
        self.logger.debug("Iterating over the measures in the data")
        for measure_index, measure_name in enumerate(self.measures):
            i = 0
            self.logger.debug("Iterating over the folders in the measure {}".format(measure_name))
            sorted_folders = {k: v for k, v in sorted(self.stat_dict[measure_name].items(),
                                                      key=lambda item: len(item[1]), reverse=True)}
            for folder_name, paths in sorted_folders.items():
                # Do not show on plot where all values are 0 or None
                if all(value == 0 or value is None for value in paths.values()):
                    continue

                sns.histplot(paths, ax=axes[measure_index, i], bins=20)
                axes[measure_index, i].set_xlabel(measure_name, color="b")
                axes[measure_index, i].set_title(folder_name, color="r")
                i += 1
                if i >= max_size:
                    self.logger.debug("Reached the maximum number of folder shown on the visualization")
                    break
        plt.tight_layout()
        self.logger.info("Plots created")

        if save_file is not None:
            self.logger.debug("Saving plot to file")
            fig.savefig(Path(save_file))
            self.logger.info("Saved plot at path {}".format(save_file))
        if show_graph:
            self.logger.debug("Displaying plots")
            plt.show()

    def create_summary(self, root, configurations):
        self.logger.debug("Initializing summary output")
        output = "***** Analysis of file structure at : '{}' *****" \
                 "\nCreated: {}\nTarget directory : {}\n\n".format(root.name, time.ctime(), root)

        if configurations is not None:
            for identifier, configuration_list in configurations.items():
                output += "\nConfigurations for folder **{}**:".format(identifier)
                sorted_config_list = [v for v in sorted(configuration_list,
                                                        key=lambda item: len(item["paths"]), reverse=True)]
                for i in range(len(sorted_config_list)):
                    output += "\n     Configuration #{} was found in {} folders. Contains the following : " \
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
            self.logger.info("Found {} folder/files for measure {}".format(len(sorted_folders), measure_name))
        self.logger.info("Summary created with {} measures. Contains {} total written characters.".format(
            len(self.measures), len(output)))
        return output

    def create_csv(self, output_path):
        self.logger.debug("Opening csv file for writing at : {}".format(output_path))
        with open(output_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            headers = ['Path'] + ['IdentifierEngine'] + list(self.measures)
            csv_writer.writerow(headers)
            self.logger.info("Storing in CSV file with header : {}".format(str(headers)))
            # Supposing every file/folder is present in the first measure's dictionary
            self.logger.debug("Iterating through every file/folder type to populate CSV.")
            for file_identifier, paths in sorted(self.stat_dict[self.measures[0]].items()):
                "For every path found in the first measure, write all the measures for that path in the same row."
                for path, value in paths.items():
                    row = list()
                    for measure in self.measures:
                        row.append(self.stat_dict[measure][file_identifier][path])
                    csv_writer.writerow([path] + [file_identifier] + row)
        self.logger.info("CSV files closed. Contains {} bytes of data".format(Path(output_path).stat().st_size))