# -*- coding: utf-8 -*-

"""
Explore a file structure and build of distribution of file numbers and file size.
"""

import argparse
from fileChecker import *
from fileTreeHandler import FileTreeHandler
from statBuilder import StatBuilder
from displayablePath import DisplayablePath
import configparser

CONFIG_PATH = "./config.ini"


def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    # The only required argument is the location of the directory to explore
    pars.add_argument('start_location', type=str, help="Directory to explore")
    return pars


def explore_template(root, template, common_key):
    # Method using templates instead of blindly iterating, NOT FINISHED
    tree = FileTreeHandler(template, root)
    tree = tree.update(common_key)

    # Iterate over the pipelines and subjects
    folders = {}
    for subject_tree in tree.iter('image1'):
        folders[str(subject_tree.get('subject_number'))] = subject_tree.get('pipeline1')
    # Run tests for each pipeline


def explore_with_generator(root, output_path=None, get_count=False, get_size=False):
    # Generate an instance of DisplayablePath for every file and folder (recursively) and store them
    paths = DisplayablePath.generate_tree(root, criteria=None)

    # Display the file tree either in the std_output or a text_file
    stat_dict = {"file_count": {}, "file_size": {}}
    if output_path is None:
        for path in paths:
            stat_dict = path.add_stats(stat_dict)
            print(path.displayable(get_count=get_count, get_size=get_size), end='')
    else:
        with open(output_path, 'wt', encoding="utf-8") as f:
            for path in paths:
                stat_dict = path.add_stats(stat_dict)
                f.write(path.displayable(get_count=get_count, get_size=get_size))
    return stat_dict


def main():
    # Parsing the config file
    config = configparser.ConfigParser()
    config.read(Path(CONFIG_PATH))
    if config['Output'].getboolean('output as file'):
        output_path = Path(config['Output']['output path'])
    else:
        output_path = None

    # Choose exploration method for the file structure
    if config['Custom Template'].getboolean('use template'):
        template = Path(config['Custom Template']['template path'])
        explore_method = 'template'
    else:
        template = None
        explore_method = 'generator'

    # Parsing arguments
    parser = _arg_parser()
    args = parser.parse_args()
    root = Path(args.start_location)

    # Verifying number of files for debug
    # print(get_file_count(root))

    # Get the data and create the file structure in console or text file
    stat_dict = {}
    if explore_method == 'template':
        explore_template(root, template, "sub-{subject_number}")  # using sub-## as the common key to explore the files

    if explore_method == 'generator':
        stat_dict = explore_with_generator(root, output_path=output_path,
                                           get_count=config['Measures'].getboolean('file count'),
                                           get_size=config['Measures'].getboolean('file size'))

    # Create a dataframe with the dicts
    stat_builder = StatBuilder(stat_dict)

    vis_config = config['Visualization']
    if vis_config.getboolean('show visualization'):
        # Show the distribution of the statistics
        stat_builder.create_graphs(["file_count", "file_size"], max_size=vis_config.getint('shown folder count'))


if __name__ == "__main__":
    main()
