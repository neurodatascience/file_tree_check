# -*- coding: utf-8 -*-

"""
Explore a file structure and build of distribution of file numbers and file size.
"""

import argparse
from fileChecker import *
from statBuilder import StatBuilder
from displayablePath import DisplayablePath
import configparser
import logging

CONFIG_PATH = "./config.ini"


def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    # The only required argument is the location of the directory to explore
    pars.add_argument('start_location', type=str, help="Directory to explore")
    pars.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                      default=False, help="Print info level logging to the console")
    return pars


def _create_logger(file_log_path, file_log_level, is_verbose):
    logger = logging.getLogger("file_tree_check")
    logger.setLevel(file_log_level.upper())
    file_format = logging.Formatter(fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                                    datefmt="%m-%d %H:%M")
    console_format = logging.Formatter(fmt="%(name)-12s %(levelname)-8s %(message)s")

    if is_verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    if str(file_log_path) != "None":
        file_handler = logging.FileHandler(file_log_path, mode="w")
        file_handler.setLevel(file_log_level.upper())
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


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

    # Parsing arguments
    parser = _arg_parser()
    args = parser.parse_args()

    # Initializing logger
    logger = _create_logger(config['Logging']['file log path'],
                            config['Logging']['file log level'], is_verbose=args.verbose)

    logger.debug("Initializing variables from arguments")
    root = Path(args.start_location)
    logger.info("Target folder is : {}".format(root))

    logger.debug("Initializing variables from config file")
    if config['Output'].getboolean('output as file'):
        output_path = Path(config['Output']['output path'])
    else:
        output_path = None
    logger.info("Output file path is : {}".format(str(output_path)))

    # Verifying number of files for debug
    # print(get_file_count(root))

    logger.debug("Launching exploration of the target folder")
    stat_dict = {}
    stat_dict = explore_with_generator(root, output_path=output_path,
                                       get_count=config['Measures'].getboolean('file count'),
                                       get_size=config['Measures'].getboolean('file size'))
    logger.info("Retrieved {} measures for {} different folders name".format(len(stat_dict),
                                                                             len(stat_dict["file_count"])))
    logger.debug("Creating a dataframe with the dicts")
    stat_builder = StatBuilder(stat_dict)
    logger.info("Created a dataframe with the measures")

    vis_config = config['Visualization']
    if vis_config.getboolean('create plots'):
        logger.debug("Giving the data to the graphic creator")
        if config["Visualization"].getboolean("save plots"):
            image_path = Path(vis_config["image path"])
        else:
            image_path = None
        stat_builder.create_graphs(["file_count", "file_size"], max_size=vis_config.getint('shown folder count'),
                                   save_file=image_path, show_graph=vis_config.getboolean("print plots"))


if __name__ == "__main__":
    main()
