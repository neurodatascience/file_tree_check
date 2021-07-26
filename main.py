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
import os


def parse_config(config_file):
    confpars = configparser.ConfigParser(config_file)


def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    # The only required argument is the location of the directory to explore
    pars.add_argument('start_location', type=str, help="Directory to explore")
    pars.add_argument('-o', '--output_location', type=str, default=None,
                      help="Directory where to place the outputs. If None is given, the output is sent "
                           "to print in the std_output.")
    pars.add_argument('-c', '--file_count', dest='file_count', action='store_true', default=False,
                      help='Will count the files in every directory.')
    pars.add_argument('-s', '--file_size', dest='file_size', action='store_true', default=False,
                      help='Will get the size of every file and the average size of the files'
                           ' directly under each directory. ')
    pars.add_argument('-g', '--graph', dest='show_graphics', action='store_true', default=False,
                      help='Print the distributions figure to the standard output.')
    pars.add_argument('--tree', type=str, default=None,
                      help="Path to the .tree template describing the file structure. "
                           "Do not include to iterate automatically over all files.")
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


def explore_with_generator(root, output_dir=None, get_count=False, get_size=False):
    # Generate an instance of DisplayablePath for every file and folder (recursively) and store them
    paths = DisplayablePath.generate_tree(root, criteria=None)

    # Display the file tree either in the std_output or a text_file
    stat_dict = {"file_count": {}, "file_size": {}}
    if output_dir is None:
        for path in paths:
            stat_dict = path.add_stats(stat_dict)
            print(path.displayable(get_count=get_count, get_size=get_size), end='')
    elif output_dir.is_dir():
        filename = "File_Structure.txt"  # Change name to an argument given by user
        with open(os.path.join(output_dir, filename), 'wt', encoding="utf-8") as f:
            for path in paths:
                stat_dict = path.add_stats(stat_dict)
                f.write(path.displayable(get_count=get_count, get_size=get_size))
    return stat_dict


def main():
    # Parsing arguments
    parser = _arg_parser()
    args = parser.parse_args()
    root = Path(str(args.start_location))
    output_dir = None
    if args.output_location is not None:
        output_dir = Path(str(args.output_location))

    # Choose exploration method for the file structure
    if args.tree is None:
        explore_method = 'generator'
        template = None
    else:
        explore_method = 'template'
        template = Path(str(args.tree))

    # Verifying number of files for debug
    print(get_file_count(root))

    # Get the data and create the file structure in console or text file
    stat_dict = {}
    if explore_method == 'template':
        explore_template(root, template, "sub-{subject_number}")  # using sub-## as the common key to explore the files

        stat_builder = StatBuilder(stat_dict)

        if args.show_graphics:
            # Show the distribution of the statistics
            stat_builder.create_graphs(["file_count"], ["file_size"])

    if explore_method == 'generator':
        stat_dict = explore_with_generator(root, output_dir=output_dir,
                                           get_count=args.file_count, get_size=args.file_size)
        # Create a dataframe with the dicts
        stat_builder = StatBuilder(stat_dict)

        if args.show_graphics:
            # Show the distribution of the statistics
            stat_builder.create_graphs(["file_count"], ["file_size"])


if __name__ == "__main__":
    main()
