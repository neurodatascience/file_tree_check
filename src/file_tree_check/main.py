"""Explore a file structure and build of distribution of file numbers and file size."""
from __future__ import annotations

import argparse
import configparser
import logging
import os
import re
from pathlib import Path

from file_tree_check.identifierEngine import IdentifierEngine
from file_tree_check.smartDirectoryPath import SmartDirectoryPath
from file_tree_check.smartFilePath import SmartFilePath
from file_tree_check.statBuilder import StatBuilder

# Edit the following line to point to the config file location in your current installation:
CONFIG_PATH = r"/home/remi/github/file_tree_check/src/file_tree_check/config.ini"
LOGGER_NAME = "file_tree_check"
LOGGER_FILE_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
LOGGER_CONSOLE_FORMAT = "%(name)-12s %(levelname)-8s %(message)s"
FILENAME_MAX_LENGTH = 60


def _arg_parser():
    """Extract the arguments given to the script.

    Arguments are the part given after the main.py call in the command line.

    Only 1 required argument:
    the path to the folder to be used as the root for the analysis.
    2 optional and mutually exclusive arguments:
    "verbose" and "debug" to print logs of various levels to the console.

    If neither "verbose" nor "debug" is given, logs will not be output
    to the console (or other standard output)
    although they could be saved in a file via an option in the config files.
    "debug" will show more detailed information to the console compared to "verbose".
    Activating the log to console with either "verbose" or "debug"
    is independent and not mutually exclusive to the logs to file.

    Returns
    -------
    argparse.ArgumentParser
        A parser object to be used in main() containing the argument data.
    """
    pars = argparse.ArgumentParser(description="Insert doc here")
    pars.add_argument("start_location", type=str, help="Directory to explore")
    console_log = pars.add_mutually_exclusive_group()
    console_log.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print info level logging to the console",
    )
    console_log.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Print debug level logging to the console",
    )
    return pars


def _create_logger(file_log_path, file_log_level, is_verbose, is_debug):
    """Instantiate the logger object that will collect and print logs during the script execution.

    File logging include the date but console logs do not.
    If is_verbose and is_debug are both false, they will be no logs printed to the console.

    Parameters
    ----------
    file_log_path: string
        The path to the file where to save the logs. If is None, will not save path to any files.
    file_log_level: string
        The level of logging for the log file.
        Either "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG" or "NOTSET".
    is_verbose: bool
        Indicate if the console logger is to be set to the "INFO" level.
    is_debug: bool
        Indicate if the console logger is to be set to the "DEBUG" level
        for more detailed console logs.

    Returns
    -------
    logging.Logger
        The logger object who will redirect the log line given
        during the script execution to the desired outputs.
    """
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


def generate_tree(
    root, parent=None, is_last=False, criteria=None, filter_files=False, filter_dir=False
):
    """Create a SmartFilePath or SmartDirectoryPath generator object \
    for every item found within the root directory.

    These generator objects will have to be iterated over
    to get the SmartPath items themselves.
    Returns an iterable of the file structure
    that can be used over each element.
    When a subdirectory is found under the given path,
    will call another instance of this method with it as the root.

    Parameters
    ----------
    root: string or pathlib.Path
        The path for which to generate the SmartPath instance and recursively run
        this function on it's children files
        and directories.
    parent: SmartPath
        The instance of the parent SmartPath.
        This reference allows the children SmartPath to calculate their depth
        relative to the first root of the file structure.
    is_last: bool
        Indicate whether or not this file/directory was the last to be generated
        in it's parent folder.
        Only relevant for visual display of the file structure.
    criteria: re.Pattern
        A regular expression compiled into a Pattern object to be used
        to filter files and/or directories included
        in the generator output. Files/directories that do not match the regular expression
        will be discarded including all their children regardless of their name for directories.
        If no criteria is given, every file and directory will be included in the generation.
    filter_files: bool
        Whether or not the search criteria will be used to discard files
        whose names do not match the regular expression.
    filter_dir: bool
        Whether or not the search criteria will be used to discard directories
        whose names do not match.

    Yields
    ------
    generator object
        Each execution of generate_tree yields a single instance
        of SmartFilePath or SmartDirectoryPath to the generator
        that will create them when iterated upon.
        However, since another generate_tree() function is called on each children found,
        while each function yield a single object,
        the end result will be that a object will be yielded for every file
        and directory found in the initial root (or for every one that matches the criteria).
        Iterating over the output generator object will then allow to act
        on a SmartPath instance of every file and
        directory after only having to call ourself generate_tree() once on the target folder.
    """
    logger = logging.getLogger(LOGGER_NAME)
    root = Path(str(root))

    # Begin by generating the root path
    smart_root = SmartDirectoryPath(root, parent, is_last)
    yield smart_root

    # Get a list of every file/directory in the root and iterate over them
    if criteria is not None:
        filtered_children = [
            path
            for path in root.iterdir()
            if criteria.match(str(path.name)) is not None
            or (path.is_dir() and not filter_dir)
            or (path.is_file() and not filter_files)
        ]
        children = sorted(filtered_children, key=lambda s: str(s).lower())
    else:
        children = sorted(list(root.iterdir()), key=lambda s: str(s).lower())

    count = 1
    for path in children:
        try:
            # Check if this path is the last children in its parent's directory
            is_last = count == len(children)
            # If the children is a directory, another instance of the method is called and
            # its output is propagated up the generator
            if path.is_dir():
                yield from generate_tree(
                    path,
                    parent=smart_root,
                    is_last=is_last,
                    criteria=criteria,
                    filter_files=filter_files,
                    filter_dir=filter_dir,
                )
            # If the children is a file,
            # generate a single instance of SmartPath associated to its path
            else:
                yield SmartFilePath(path, smart_root, is_last)
            count += 1
        except FileNotFoundError as e:
            logger.warning("FileNotFoundError", e)
            continue


def get_data_from_paths(
    paths,
    identifier,
    output_path=None,
    measures=(),
    get_configurations=False,
    target_depth=None,
    pipe_file_data=False,
):
    """Iterate over each file/directory in the generator to get measure and, \
    create the file tree  if requested.

    Parameters
    ----------
    paths: iterable containing SmartPath objects
        Expected to be the generator object created by generate_tree()
        but can theoretically be any iterable containing SmartPath objects.
    identifier: IdentifierEngine
        Used to extract the identifier of each path to aggregate it
        with similar ones resent in the file structure.
        This IdentifierEngine is also passed to add_configuration
        to allow it to extract identifiers as well.
    output_path: pathlib.Path
        The path to the text file where the file tree output will be saved.
        If none, the type of output is skipped.
    measures: list of string
        The name of the measures to be used in the outputs.
        Each corresponds to a dictionary nested in stat_dict.
    get_configurations: bool
        Whether or not to compare the configuration of the folders in the repeating structure.
    target_depth: int
        Passed to add_configuration() to specify which depth of folder
        to use for configuration comparison.
    pipe_file_data: bool
        Whether to output the data from each file found directly
        to the standard output during the execution.
        By default this will print in the console which is not recommended for large dataset.
        If the script is followed by a pipe, this will pass the data to the other script or command.
        Only outputs files because directories shouldn't be relevant for the custom tests.
        Outputted format is  a single string per file in the format:
        'path,identifier,file_size,modified_time'.
        File_size is in bytes, modified_time is in seconds (epoch time).

    Returns
    -------
    stat_dict: dict
    The dictionary containing the the values for each measures.
        stat_dict contains nested dictionaries with the following structure:
        stat_dict={
            'measure1':
                {'identifier1': {
                    'path1': value, 'path2': value, ...},
                'identifier2': {
                    'path3': value, 'path4': value}, ...},
                }
            'measure2':
                {'identifier1': {}, 'identifier2': {}, ...}
            }
    configurations: dict
        Contains the file configurations found for each file/directory identifier
        with the following structure:
            configurations={
                'identifier1':
                    [ {'structure': ['identifier3', 'identifier4', 'identifier5'],
                                      'paths': ['path1', 'path2']},
                    {'structure': ['identifier3', 'identifier5'], 'paths': ['path4']},
                    ... ]
                'identifier2':
                    [{'structure': [], 'paths': []}, ...]
                }
    """
    configurations = {}
    stat_dict = {measure_name: {} for measure_name in measures}
    if output_path is None:
        for path in paths:
            stat_dict = path.add_stats(
                stat_dict, identifier.get_identifier(path), measures=measures
            )
            if get_configurations:
                configurations = add_configuration(
                    path, configurations, identifier, target_depth=target_depth
                )
            if pipe_file_data:
                if isinstance(path, SmartFilePath):
                    print(
                        f"{path.path},{identifier.get_identifier(path.path)},"
                        f"{path.file_size},{path.modified_time}"
                    )
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            for path in paths:
                stat_dict = path.add_stats(
                    stat_dict, identifier.get_identifier(path.path), measures=measures
                )
                if get_configurations:
                    configurations = add_configuration(
                        path, configurations, identifier, target_depth=target_depth
                    )
                f.write(path.displayable(measures=measures, name_max_length=FILENAME_MAX_LENGTH))
                if pipe_file_data:
                    if isinstance(path, SmartFilePath):
                        print(
                            f"{path.path},{identifier.get_identifier(path.path)},"
                            f"{path.file_size},{path.modified_time}"
                        )
    return stat_dict, configurations


def add_configuration(path, configurations, identifier, target_depth=None):
    """For each directory look at how it's content is structured and save \
       that structure as a configuration.

    Only compare directory of a specific depth relative to the original target directory.
    This prevents computing configurations for folder that aren't relevant
    since we are expecting the repeating
    file structure to have each unit we want to compare at the same depth in the file structure.

    Parameters
    ----------
    path: SmartPath
    configurations: dict
        Contains the file configurations found for each file/directory identifier
        with the following structure:

        .. code-block:: python

                configurations={
                    'identifier1':
                        [ {'structure': ['identifier3', 'identifier4', 'identifier5'],
                                            'paths': ['path1', 'path2']},
                        {'structure': ['identifier3', 'identifier5'], 'paths': ['path4']},
                        ... ]
                    'identifier2':
                        [{'structure': [], 'paths': []}, ...]
                    }

    identifier: IdentifierEngine
        Used to extract the identifier of each path to aggregate it with similar ones resent
        in the file structure.
    target_depth: int
        The depth at which the repeating directories for which
        to compare their configuration will be.
        Any directory found at a different depth will be ignored by this function.

    Returns
    -------
    configurations: dict
        The updated dict now containing the configuration data \
        from the path that was given as parameter.
    """
    # The root is skipped since it is alone at his target_depth level
    # and thus can't be compared
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
        # For the list of every children in the directory,
        # we don't include the parent directory prefix
        children_list.append(
            identifier.get_identifier(children_path, prefix_file_with_parent_directory=False)
        )
        children_list.sort()

    # Compare that organisation with others already found
    # The list of children is the key of the dict and the value
    # is a list of every path with that configuration
    if len(configurations[path_unique_identifier]) == 0:
        # configurations has a list of every configuration associated
        # to every identifier, each element of the list
        # is a dict containing the list of children and the path to all directories
        # following this configuration
        configurations[path_unique_identifier] = [
            {"structure": children_list, "paths": [str(path.path)]}
        ]
    else:
        # Searching if current configuration has already been seen
        for configuration in configurations[path_unique_identifier]:
            if configuration["structure"] == children_list:
                # If the configuration is known, add the current path
                # to the list of that configuration
                configuration["paths"].append(str(path.path))
                return configurations
        # if no match were found, a new configuration is added
        # to the identifier's list of configurations
        configurations[path_unique_identifier].append(
            {"structure": children_list, "paths": [str(path.path)]}
        )

    return configurations


def main():
    """Execute sequence of the script."""
    # Parsing the config file
    config = configparser.ConfigParser()
    config.read(Path(CONFIG_PATH))

    # Parsing arguments
    parser = _arg_parser()
    args = parser.parse_args()

    # Initializing logger
    logger = _create_logger(
        config["Logging"]["file log path"],
        config["Logging"]["file log level"],
        is_verbose=args.verbose,
        is_debug=args.debug,
    )

    logger.debug("Initializing variables from arguments")
    root = Path(args.start_location)
    logger.info(f"Target directory is: {root}")

    logger.debug("Initializing variables from config file")
    identifier = IdentifierEngine(
        config["Categorization"]["regular expression for file identifier"],
        config["Categorization"]["regular expression for directory identifier"],
    )

    if config["Search Criteria"].getboolean("use search criteria"):
        criteria = config["Search Criteria"]["regular expression for search criteria"]
        filter_files = config["Search Criteria"].getboolean("filter files")
        filter_dir = config["Search Criteria"].getboolean("filter directories")
        try:
            criteria = re.compile(criteria)
        except TypeError as e:
            logger.warning(f"Search Criteria {criteria} is invalid, resuming without criteria: {e}")
            criteria = None
    else:
        criteria = None
        filter_files = False
        filter_dir = False

    if config["Output"].getboolean("create summary"):
        summary_output_path = Path(config["Output"]["summary output path"])
    else:
        summary_output_path = None

    if config["Output"].getboolean("create text tree"):
        tree_output_path = Path(config["Output"]["tree output path"])
    else:
        tree_output_path = None

    if config["Output"].getboolean("create csv"):
        csv_output_path = Path(config["Output"]["csv output path"])
    else:
        csv_output_path = None

    if config["Configurations"].getboolean("get number of unique configurations"):
        get_configurations = True
        target_depth = config["Configurations"].getint("target depth")
    else:
        get_configurations = False
        target_depth = -1

    logger.info(
        f"Output file paths: Summary:'{str(summary_output_path)}', "
        f"Tree:'{str(tree_output_path)}', CSV:'{str(csv_output_path)}'"
    )

    logger.debug("Launching exploration of the target directory")
    measure_list = [key for key in config["Measures"] if config["Measures"].getboolean(key)]
    paths = generate_tree(root, criteria=criteria, filter_files=filter_files, filter_dir=filter_dir)
    stat_dict, configurations = get_data_from_paths(
        paths,
        identifier,
        output_path=tree_output_path,
        measures=measure_list,
        get_configurations=get_configurations,
        target_depth=target_depth,
        pipe_file_data=config["Pipeline"].getboolean("pipe file data"),
    )
    logger.info(
        f"Retrieved {len(stat_dict)} measures for "
        f"{len(stat_dict['file_count'])} different directory name"
    )
    logger.debug("Creating instance of StatBuilder with the measures")
    stat_builder = StatBuilder(stat_dict, measure_list)

    vis_config = config["Visualization"]
    if vis_config.getboolean("create plots"):
        logger.debug("Giving the data to the graphic creator")
        if vis_config.getboolean("save plots"):
            image_path = Path(vis_config["image path"])
        else:
            image_path = None
        stat_builder.create_plots(
            plots_per_measure=vis_config.getint("number of plot per measure"),
            save_path=image_path,
            show_plot=vis_config.getboolean("print plots"),
        )

    if summary_output_path is not None:
        logger.debug("Launching summary text output generation.")
        with open(summary_output_path, "w", encoding="utf-8") as f:
            f.write(stat_builder.create_summary(root, configurations))

    if csv_output_path is not None:
        logger.debug("Launching CSV output generation.")
        stat_builder.create_csv(csv_output_path)

    logger.info("Script executed successfully.")


if __name__ == "__main__":
    main()
