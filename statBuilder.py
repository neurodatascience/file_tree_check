import logging
import operator
from collections import Counter
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path

FIG_SIZE = (20, 12)


class StatBuilder(object):
    """
    Store the data in a dictionary and create histograms of the distribution of the data for each folder.
    """

    def __init__(self, stat_dict):
        self.stat_dict = stat_dict
        self.logger = logging.getLogger("file_tree_check.{}".format(__name__))
        self.logger.info("Created an instance of statBuilder")

    def create_graphs(self, measures_list=(), save_file=None, show_graph=True, max_size=8):
        """Will create a comparison graph for each measure given in a single figure."""
        sns.set(style="darkgrid")
        self.logger.debug("Creating subplots objects")
        height = len(measures_list)
        fig, axes = plt.subplots(height, max_size, figsize=FIG_SIZE)
        fig.suptitle('Distribution in the file structure')
        self.logger.debug("Iterating over the measures in the data")
        for measure_index, measure_name in enumerate(measures_list):
            i = 0
            self.logger.debug("Iterating over the folders in the measure {}".format(measure_name))
            sorted_folders = {k: v for k, v in sorted(self.stat_dict[measure_name].items(),
                                                      key=lambda item: len(item[1]), reverse=True)}
            for folder_name, paths in sorted_folders.items():
                # Do not show on plot folders where all values are 0
                if max(paths.values()) <= 0:
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

    def create_summary(self, measures_list=()):
        self.logger.debug("Initializing summary output")
        output = ""
        for measure_name in measures_list:
            output += "Occurrences for measure  : {}\n".format(measure_name)
            sorted_folders = {k: v for k, v in sorted(self.stat_dict[measure_name].items(),
                                                      key=lambda item: len(item[1]), reverse=True)}
            for folder_name, paths in sorted_folders.items():
                most_common_value, most_common_counter = 0, 0
                output += "    In folders named {} :\n".format(folder_name)
                counter = Counter()
                for path, value in paths.items():
                    counter[value] += 1
                most_common_value = counter.most_common(1)[0][0]
                most_common_counter = counter.most_common(1)[0][1]
                output += "        Most common : {} found in {} folders\n".format(most_common_value,
                                                                                  most_common_counter)
                self.logger.debug("Calculating occurrences different from most "
                                  "common value {} in folders named {}".format(most_common_value, most_common_counter))
                if most_common_counter < len(paths):
                    output += "        Outliers :\n"
                    for path, value in paths.items():
                        if value != most_common_value:
                            output += "            {}  has : {}\n".format(str(path), value)

        return output