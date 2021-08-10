import logging
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

    def create_graphs(self, measures_list, save_file=None, show_graph=True, max_size=8):
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
            for folder_name, values in sorted_folders.items():
                if max(values) <= 0:
                    continue
                sns.histplot(values, ax=axes[measure_index, i], bins=20)
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
