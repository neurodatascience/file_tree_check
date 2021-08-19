# -*- coding: utf-8 -*-

"""
Explore a file structure and build of distribution of file numbers and file size.
"""

import argparse
from fileChecker import *
from statBuilder import StatBuilder
from smartPath import SmartPath
from smartFilePath import SmartFilePath
from smartDirectoryPath import SmartDirectoryPath
import configparser
import logging

CONFIG_PATH = "config.ini"
LOGGER_NAME = "file_tree_check"
LOGGER_FILE_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
LOGGER_CONSOLE_FORMAT = "%(name)-12s %(levelname)-8s %(message)s"
FILENAME_MAX_LENGTH = 60


def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    # The only required argument is the location of the directory to explore
    pars.add_argument('start_location', type=str, help="Directory to explore")
    pars.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                      default=False, help="Print info level logging to the console")
    return pars


def _create_logger(file_log_path, file_log_level, is_verbose):
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(file_log_level.upper())
    file_format = logging.Formatter(fmt=LOGGER_FILE_FORMAT, datefmt="%m-%d %H:%M")
    console_format = logging.Formatter(fmt=LOGGER_CONSOLE_FORMAT)

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


def explore_with_generator(root, output_path=None, measures=(), separator="_"):
    # Generate an instance of SmartPath for every file and folder (recursively) and store them
    paths = generate_tree(root, criteria=None)

    # Display the file tree either in the std_output or a text_file and get the measures on each file/folder
    stat_dict = {}
    for measure_name in measures:
        stat_dict[measure_name] = {}
    if output_path is None:
        for path in paths:
            stat_dict = path.add_stats(stat_dict, separator=separator)
            print(path.displayable(measures=measures, name_max_length=FILENAME_MAX_LENGTH), end='')
    else:
        with open(output_path, 'wt', encoding="utf-8") as f:
            for path in paths:
                stat_dict = path.add_stats(stat_dict, measures=measures, separator=separator)
                f.write(path.displayable(measures=measures, name_max_length=FILENAME_MAX_LENGTH))
    return stat_dict


def generate_tree(root, parent=None, is_last=False, criteria=None):
    """Generator that creates a SmartFilePath or SmartDirectoryPath object for every item found
    within the root directory given.
    Returns an iterable of the file structure that can be used with display() over each element.
    When a subdirectory is found under the given path, will call another instance of this method with it as the root
    """
    logger = logging.getLogger(LOGGER_NAME)
    root = Path(str(root))
    # A criteria could be used to ignore specific files or folder
    criteria = criteria or SmartPath.default_criteria

    # Begin by generating the root path
    smart_root = SmartDirectoryPath(root, parent, is_last)
    yield smart_root

    # Get a list of every files or folder in the root and iterate over them
    children = sorted(list(path for path in root.iterdir()), key=lambda s: str(s).lower())
    count = 1
    for path in children:
        try:
            # Check if this path is the last children in its parent's directory
            is_last = count == len(children)
            # If the children is a folder, another instance of the method is called and
            # its output is propagated up the generator
            if path.is_dir():
                yield from generate_tree(path, parent=smart_root,
                                         is_last=is_last, criteria=criteria)
            # If the children is a file, generate a single instance of SmartPath associated to its path
            else:
                yield SmartFilePath(path, smart_root, is_last)
            count += 1
        except FileNotFoundError as e:
            logger.error("FileNotFoundError", e)


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
    if config['Output'].getboolean('create text files'):
        tree_output_path = Path(config['Output']['tree output path'])
        summary_output_path = Path(config['Output']['summary output path'])
    else:
        tree_output_path = None
        summary_output_path = None
    logger.info("Output file path are : {}, {}".format(str(tree_output_path), str(summary_output_path)))

    # Verifying number of files for debug
    # print(get_total_file_count(root))

    logger.debug("Launching exploration of the target folder")
    measure_list = []
    for key in config["Measures"]:
        if config["Measures"].getboolean(key):
            measure_list.append(key)

    stat_dict = explore_with_generator(root, output_path=tree_output_path, measures=measure_list,
                                       separator=config['Categorization']['separator'])
    logger.info("Retrieved {} measures for {} different folders name".format(len(stat_dict),
                                                                             len(stat_dict["file_count"])))
    logger.debug("Creating instance of StatBuilder with the measures")
    stat_builder = StatBuilder(stat_dict)

    vis_config = config['Visualization']
    if vis_config.getboolean('create plots'):
        logger.debug("Giving the data to the graphic creator")
        if vis_config.getboolean("save plots"):
            image_path = Path(vis_config["image path"])
        else:
            image_path = None
        stat_builder.create_graphs(max_size=vis_config.getint('shown folder count'),
                                   save_file=image_path, show_graph=vis_config.getboolean("print plots"))

    if summary_output_path is not None:
        with open(summary_output_path, 'wt', encoding="utf-8") as f:
            f.write(stat_builder.create_summary())


if __name__ == "__main__":
    main()
