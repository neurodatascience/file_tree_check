import logging
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path



class StatBuilder(object):
    """
    Store the data in a dataframe and create histograms of the distribution of the data for each folder.
    """

    def __init__(self, stat_dict):
        self.dataframe = pd.DataFrame(stat_dict)
        self.logger = logging.getLogger("file_tree_check.{}".format(__name__))
        self.logger.info("Created an instance of statBuilder")

    def create_graphs(self, columns_list, save_file=None, show_graph=True, max_size=8):
        """Will create a comparison graph for each column given in a single figure."""
        self.logger.debug("Creating subplots objects")
        height = len(columns_list)
        fig, axes = plt.subplots(height, max_size, sharey='row')
        fig.suptitle('Distribution in the file structure')
        self.logger.debug("Iterating over the measures in the data")
        for column_index, column_name in enumerate(columns_list):
            i = 0
            self.logger.debug("Iterating over the folders in the measure {}".format(column_name))
            for folder_name, values in self.dataframe[column_name].items():
                if max(values) <= 0:
                    continue
                sns.histplot(values, ax=axes[column_index, i], kde=False)
                axes[column_index, i].set(xlabel=column_name, title=folder_name)
                i += 1
                if i >= max_size:
                    self.logger.debug("Reached the maximum number of folder shown on the visualization")
                    break
        self.logger.info("Plots created")
        if save_file is not None:
            self.logger.debug("Saving plot to file")
            fig.savefig(Path(save_file))
            self.logger.info("Saved plot at path {}".format(save_file))
        if show_graph:
            self.logger.debug("Displaying plots")
            plt.tight_layout()
            plt.show()
