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
from identifierEngine import IdentifierEngine
import configparser
import logging
import re

CONFIG_PATH = r"C:\Users\datbo\PycharmProjects\testNeuro\src\file_tree_check\config.ini"
LOGGER_NAME = "file_tree_check"
LOGGER_FILE_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
LOGGER_CONSOLE_FORMAT = "%(name)-12s %(levelname)-8s %(message)s"
FILENAME_MAX_LENGTH = 60


def _arg_parser():
    pars = argparse.ArgumentParser(description="Insert doc here")
    # The only required argument is the location of the directory to explore
    pars.add_argument('start_location', type=str, help="Directory to explore")
    console_log = pars.add_mutually_exclusive_group()
    console_log.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                             default=False, help="Print info level logging to the console")
    console_log.add_argument('-d', '--debug', dest="debug", action='store_true',
                             default=False, help="Print debug level logging to the console")
    return pars


def _create_logger(file_log_path, file_log_level, is_verbose, is_debug):
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(file_log_level.upper())
    file_format = logging.Formatter(fmt=LOGGER_FILE_FORMAT, datefmt="%m-%d %H:%M")
    console_format = logging.Formatter(fmt=LOGGER_CONSOLE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)
    if is_verbose:
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    elif is_debug:
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

    if str(file_log_path) != "None":
        file_handler = logging.FileHandler(file_log_path, mode="w")
        file_handler.setLevel(file_log_level.upper())
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def generate_tree(root, parent=None, is_last=False, criteria=None):
    """Generator that creates a SmartFilePath or SmartDirectoryPath object for every item found
    within the root directory given.
    Returns an iterable of the file structure that can be used with display() over each element.
    When a subdirectory is found under the given path, will call another instance of this method with it as the root
    """
    logger = logging.getLogger(LOGGER_NAME)
    root = Path(str(root))
    # A criteria can be used to ignore specific files or directories
    if criteria is not None:
        try:
            criteria = re.compile(criteria)
        except TypeError as e:
            logger.warning("Search Criteria {} is invalid, resuming without criteria : {}".format(criteria, e))
            criteria = None

    # Begin by generating the root path
    smart_root = SmartDirectoryPath(root, parent, is_last)
    yield smart_root

    # Get a list of every file/directory in the root and iterate over them
    if criteria is not None:
        children = sorted(list(path for path in root.iterdir() if criteria.match(str(path.name)) is not None), key=lambda s: str(s).lower())
    else:
        children = sorted(list(path for path in root.iterdir()), key=lambda s: str(s).lower())

    count = 1
    for path in children:
        try:
            # Check if this path is the last children in its parent's directory
            is_last = count == len(children)
            # If the children is a directory, another instance of the method is called and
            # its output is propagated up the generator
            if path.is_dir():
                yield from generate_tree(path, parent=smart_root, is_last=is_last)
            # If the children is a file, generate a single instance of SmartPath associated to its path
            else:
                yield SmartFilePath(path, smart_root, is_last)
            count += 1
        except FileNotFoundError as e:
            logger.warning("FileNotFoundError", e)
            continue


def explore_with_generator(root, criteria=None):
    """ Generate an instance of SmartPath for every file and directory (recursively) and store them"""
    return generate_tree(root, criteria=criteria)


def get_data_from_paths(paths, identifier, output_path=None, measures=(), get_configurations=False, target_depth=None):
    """Get the measures on each file/directory and create the file tree as you go if requested"""
    logger = logging.getLogger(LOGGER_NAME)
    stat_dict = {}
    configurations = {}
    for measure_name in measures:
        stat_dict[measure_name] = {}
    if output_path is None:
        for path in paths:
            stat_dict = path.add_stats(stat_dict, identifier.get_identifier(path), measures=measures)
            if get_configurations:
                configurations = add_configuration(path, configurations, identifier, target_depth=target_depth)
            print(path.displayable(measures=measures, name_max_length=FILENAME_MAX_LENGTH), end='')
    else:
        with open(output_path, 'wt', encoding="utf-8") as f:
            for path in paths:
                stat_dict = path.add_stats(stat_dict, identifier.get_identifier(path.path), measures=measures)
                if get_configurations:
                    configurations = add_configuration(path, configurations, identifier, target_depth=target_depth)
                f.write(path.displayable(measures=measures, name_max_length=FILENAME_MAX_LENGTH))
    return stat_dict, configurations


def add_configuration(path, configurations, identifier, target_depth=None):
    """For each directory (excluding root) look at how it's content is structured and save that structure as a configuration.
    """
    logger = logging.getLogger(LOGGER_NAME)
    # The root is skipped since it is alone at his target_depth level and thus can't be compared
    # and files are skipped
    if isinstance(path, SmartFilePath) or path.depth == 0:
        return configurations
    # If a target depth is given, we exclude directories from other depth levels
    path_unique_identifier = identifier.get_identifier(path.path)
    if target_depth is not None:
        if path.depth != target_depth:
            return configurations
    if path_unique_identifier not in configurations:
        configurations[path_unique_identifier] = []
    # Extract the organisation of the directory
    children_list = []
    for children in os.listdir(path.path):
        children_path = path.path.joinpath(children)
        # For the list of every children in the directory, we don't include the parent directory prefix
        children_list.append(identifier.get_identifier(children_path, prefix_file_with_parent_directory=False))
        children_list.sort()

    # Compare that organisation with others already found
    # The list of children is the key of the dict and the value is a list of every path with that configuration
    if len(configurations[path_unique_identifier]) == 0:
        # configurations has a list of every configuration associated to every identifier, each element of the list
        # is a dict containing the list of children and the path to all directories following this configuration
        configurations[path_unique_identifier] = [{"structure": children_list, "paths" : [str(path.path)]}]
        return configurations
    else:
        # Searching if current configuration has already been seen
        for configuration in configurations[path_unique_identifier]:
            if configuration["structure"] == children_list:
                # If the configuration is known, add the current path to the list of that configuration
                configuration["paths"].append(str(path.path))
                return configurations
        # if no match were found, a new configuration is added to the identifier's list of configurations
        configurations[path_unique_identifier].append({"structure": children_list, "paths": [str(path.path)]})
        return configurations


def main():
    # Parsing the config file
    config = configparser.ConfigParser()
    config.read(Path(CONFIG_PATH))

    # Parsing arguments
    parser = _arg_parser()
    args = parser.parse_args()

    # Initializing logger
    logger = _create_logger(config['Logging']['file log path'], config['Logging']['file log level'],
                            is_verbose=args.verbose, is_debug=args.debug)

    logger.debug("Initializing variables from arguments")
    root = Path(args.start_location)
    logger.info("Target directory is : {}".format(root))

    logger.debug("Initializing variables from config file")
    if config['Output'].getboolean('create text files'):
        tree_output_path = Path(config['Output']['tree output path'])
        summary_output_path = Path(config['Output']['summary output path'])
    else:
        tree_output_path = None
        summary_output_path = None

    if config['Output'].getboolean('create csv'):
        csv_output_path = Path(config['Output']['csv output path'])
    else:
        csv_output_path = None
    identifier = IdentifierEngine(config["Categorization"]["regular expression for file identifier"],
                                  config["Categorization"]["regular expression for directory identifier"])

    if config["Search Criteria"].getboolean("use search criteria"):
        criteria = config["Search Criteria"]["regular expression for search criteria"]
    else:
        criteria = None

    logger.info("Output file paths, Tree:{}, Summary:{}, CSV:{}".format(str(tree_output_path), str(summary_output_path),
                                                                        str(csv_output_path)))

    logger.debug("Launching exploration of the target directory")
    measure_list = []
    for key in config["Measures"]:
        if config["Measures"].getboolean(key):
            measure_list.append(key)

    paths = explore_with_generator(root, criteria=criteria)
    stat_dict, configurations = get_data_from_paths(paths,
                                                    identifier, output_path=tree_output_path, measures=measure_list,
                                                    get_configurations=config['Configurations']
                                                    .getboolean("get number of unique configurations"),
                                                    target_depth=config['Configurations'].getint('target depth'))
    logger.info("Retrieved {} measures for {} different directory name".format(len(stat_dict),
                                                                               len(stat_dict["file_count"])))
    logger.debug("Creating instance of StatBuilder with the measures")
    stat_builder = StatBuilder(stat_dict, measure_list)

    vis_config = config['Visualization']
    if vis_config.getboolean('create plots'):
        logger.debug("Giving the data to the graphic creator")
        if vis_config.getboolean("save plots"):
            image_path = Path(vis_config["image path"])
        else:
            image_path = None
        stat_builder.create_plots(plots_per_measure=vis_config.getint('shown directory count'),
                                  save_path=image_path, show_plot=vis_config.getboolean("print plots"))

    if summary_output_path is not None:
        with open(summary_output_path, 'wt', encoding="utf-8") as f:
            f.write(stat_builder.create_summary(root, configurations))

    if csv_output_path is not None:
        stat_builder.create_csv(csv_output_path)

    if config["Pipeline"].getboolean("pipe file data at end of execution") is True:
        """After the successful execution of the script, the output can be outputted in the standard output.
        By default this will print in the console which is not recommended for large dataset if given a pipe, this will
        pass the data to the other script or command.
        Only outputs the files currently because directories shouldn't be relevant for the custom tests.
        Outputted format is  a single line per file : 'path,identifier,file_size,modified_time'. """
        if config["Pipeline"].getboolean("ask confirmation") is True:
            logger.debug("Giving the data of every file to the standard output")
            confirm = input('All outputs created. Do you wish to send the data to the standard output? (y/n)').lower()
            if confirm.startswith('y'):
                for path in paths:
                    if isinstance(path, SmartPath):
                        print(path.path + ',' + identifier.get_identifier(path.path) + ',' + path.file_size
                              + ',' + path.modified_time)
                logger.info("File data was given to standard output.")

    logger.info("Script executed successfully.")


if __name__ == "__main__":
    main()
