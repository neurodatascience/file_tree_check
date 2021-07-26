import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path


class StatBuilder():
    """
    Store the data in a dataframe and create histograms of the distribution of the data for each folder.
    """

    def __init__(self, stat_dict):
        self.dataframe = pd.DataFrame(stat_dict)

    def create_graphs(self, columns_list, save_file=None, show_graph=True, max_size=8, fig_size=(18, 8)):
        """Will create a comparison graph for each column given in a single figure."""
        height = len(columns_list)
        fig, axes = plt.subplots(height, max_size, sharey='row', fig_size=fig_size)
        fig.suptitle('Distribution in the file structure')
        for column_index, column_name in enumerate(columns_list):
            i = 0
            for folder_name, values in self.dataframe[column_name].items():
                if max(values) <= 0:
                    continue
                sns.histplot(values, ax=axes[column_index, i], discrete=True, kde=True)
                axes[column_index, i].set(xlabel=column_name, title=folder_name)
                i += 1
                if i >= max_size:
                    break
        if save_file is not None:
            plt.savefig(Path(save_file))
        if show_graph:
            plt.show()
