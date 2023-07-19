from __future__ import annotations

import argparse
import configparser
from pathlib import Path


class Parser:
    """Class to parse command line arguments and configuration file."""

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.ini"

    def __init__(self) -> None:
        # Search Criteria
        self.use_search = False
        self.search_expression = ""
        # Filtering
        self.filter_files = False
        self.filter_directories = False
        self.filter_hidden = False
        self.filter_custom = False
        self.filter_custom_list = ""
        # Measures
        self.file_count = False
        self.dir_count = False
        self.file_size = False
        self.file_size_rounding_percentage = 0
        self.modified_time = False
        self.modified_time_rounding_margin = 0
        self.measures = []
        # Output
        self.create_summary = False
        self.summary_path = None
        self.create_tree = False
        self.tree_path = None
        self.create_csv = False
        self.csv_path = None
        self.create_plots = False
        self.plots_path = None
        self.num_plots = 0
        self.print_plots = False
        self.save_plots = False
        self.pipe_data = False
        # Configurations
        self.get_configurations = False
        self.target_depth = -1
        self.use_depth_range = False
        self.range_start = -1
        self.range_end = -1
        self.limit_depth = False
        self.depth_limit = -1
        # Logging
        self.log_level = 0
        self.log_path = ""
        self.verbose = False
        self.debug = False
        # Input
        self.root_path = ""
        self.file_tree_path = ""
        # To Be Deprecated
        self.regex_file = ""
        self.regex_directory = ""
        self.check_file = False

    def make_parser(self, config_path: Path | str = None):
        parser = self.pars_args()
        args = parser.parse_args()
        if args.config is not None:
            self.pars_config(args.config)
        else:
            self.pars_config(config_path)
        self.resolve_pars(args)
        return self

    def pars_args(
        self,
    ) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", type=str, help="Path to configuration file.")
        parser.add_argument("-r", "--root", type=str, help="Path to root directory to be explored.")
        parser.add_argument("-f", "--file_tree", type=str, help="Path to file tree to be used.")
        # Only ask for search criteria if none given assume option is off,
        #  as search does not work, won't add for now
        # parser.add_argument("-s", "--search", type=str,
        #  help="Regular expression to be used as search criteria.")
        parser.add_argument("-ff", "--filter_files", help="Filter files.", action="store_true")
        parser.add_argument(
            "-fd", "--filter_directories", help="Filter directories.", action="store_true"
        )
        parser.add_argument(
            "-fh",
            "--filter_hidden",
            help="Filter hidden files and directories.",
            action="store_true",
        )
        # Only ask for list of files and directories to be ignored,
        #  if none given assume option is off
        parser.add_argument(
            "-fc", "--filter_custom", help="List of files and directories to be ignored by program."
        )
        # Measures
        parser.add_argument(
            "-mfc",
            "--file_count",
            help="If toggled then file_count measure will on.",
            action="store_true",
        )
        parser.add_argument(
            "-mdc",
            "--dir_count",
            help="If toggled then dir_count measure will on.",
            action="store_true",
        )
        parser.add_argument(
            "-ms",
            "--file_size",
            help="If toggled then file_size measure will on.",
            action="store_true",
        )
        parser.add_argument(
            "-mt",
            "--modified_time",
            help="If toggled then modified_time measure will on.",
            action="store_true",
        )
        parser.add_argument(
            "-mtr",
            "--time_round",
            type=int,
            help="Specify rounding margin for modified time measurement.(in seconds)",
        )
        parser.add_argument(
            "-msr",
            "--size_rounding",
            type=float,
            help="Specify rounding percentage for file size measurement.",
        )
        # Output
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Path to output directory. Relevant output files will be overwritten/created.",
        )
        parser.add_argument(
            "-os",
            "--summary",
            help="If toggled then summary file will be created.",
            action="store_true",
        )
        parser.add_argument(
            "-ot",
            "--tree",
            help="If toggled then text tree file will be created.",
            action="store_true",
        )
        parser.add_argument(
            "-oc", "--csv", help="If toggled then csv file will be created.", action="store_true"
        )
        # plots commands to be added later
        parser.add_argument(
            "-p",
            "--pipe_data",
            help="If toggled then data will be piped to stdout.",
            action="store_true",
        )
        # Configurations
        parser.add_argument(
            "-gc",
            "--get_configurations",
            help="If toggled then directory content configurations will be compared.",
            action="store_true",
        )
        parser.add_argument(
            "-td",
            "--target_depth",
            type=int,
            help="Specify target depth for directory content configurations.",
        )
        parser.add_argument(
            "-dr",
            "--depth_range",
            type=int,
            nargs=2,
            help="Specify range of depths for directory exploration.",
        )
        parser.add_argument(
            "-dl", "--depth_limit", type=int, help="Specify depth limit for directory exploration."
        )
        # Logging
        parser.add_argument("-l", "--log", type=str, help="Path to log file.")
        parser.add_argument("-ll", "--log_level", type=int, help="Specify log level.")
        parser.add_argument(
            "-v", "--verbose", help="If toggled then verbose mode will be on.", action="store_true"
        )
        parser.add_argument(
            "-d", "--debug", help="If toggled then debug mode will be on.", action="store_true"
        )
        return parser

    def pars_config(self, config_path: Path | str = None):
        if config_path is None:
            config_path = self.DEFAULT_CONFIG_PATH
        elif config_path is str:
            config_path = Path(config_path)
        config = configparser.ConfigParser()
        config.read(config_path)
        # Search Criteria
        self.use_search = config["Search_Criteria"].getboolean("use_search_criteria")
        self.search_expression = config["Search_Criteria"]["regular_expression_search_criteria"]
        # Filtering
        self.filter_files = config["Filter"].getboolean("filter_files")
        self.filter_directories = config["Filter"].getboolean("filter_directories")
        if not self.use_search:
            self.search_expression = None
            self.filter_files = False
            self.filter_directories = False
        self.filter_hidden = config["Filter"].getboolean("filter_hidden")
        self.filter_custom = config["Filter"].getboolean("filter_custom")
        self.filter_custom_list = config["Filter"]["filter_custom_list"]
        # Measures
        self.file_count = config["Measures"].getboolean("file_count")
        self.dir_count = config["Measures"].getboolean("dir_count")
        self.file_size = config["Measures"].getboolean("file_size")
        self.file_size_rounding_percentage = config["Measures_Averaging"].getfloat(
            "size_rounding_percentage"
        )
        self.modified_time = config["Measures"].getboolean("modified_time")
        self.modified_time_rounding_margin = config["Measures_Averaging"].getint(
            "time_rounding_seconds"
        )
        # Output
        self.create_summary = config["Output"].getboolean("create_summary")
        self.summary_path = config["Output"]["summary_path"]
        self.create_tree = config["Output"].getboolean("create_text_tree")
        self.tree_path = config["Output"]["text_tree_path"]
        self.create_csv = config["Output"].getboolean("create_csv")
        self.csv_path = config["Output"]["csv_path"]
        self.create_plots = config["Output.Visualization"].getboolean("create_plots")
        self.plots_path = config["Output.Visualization"]["plots_path"]
        self.num_plots = config["Output.Visualization"].getint("num_plots_per_measure")
        self.print_plots = config["Output.Visualization"].getboolean("print_plots")
        self.save_plots = config["Output.Visualization"].getboolean("save_plots")
        self.pipe_data = config["Output.Piping"].getboolean("pipe_data")
        # Configurations
        self.get_configurations = config["Configurations"].getboolean("get_configurations")
        self.target_depth = config["Configurations"].getint("target_depth")
        self.use_depth_range = config["Configurations"].getboolean("use_depth_range")
        self.range_start = config["Configurations"].getint("range_start")
        self.range_end = config["Configurations"].getint("range_end")
        self.limit_depth = config["Configurations"].getboolean("limit_depth")
        self.depth_limit = config["Configurations"].getint("depth_limit")
        # Logging
        self.log_level = config["Logging"]["log_level"]
        self.log_path = config["Logging"]["log_path"]
        # Input
        self.root_path = config["Input"]["root_path"]
        self.file_tree_path = config["Input"]["file_tree_path"]
        # To Be Deprecated
        self.regex_file = config["Categorization"]["regular_expression_file"]
        self.regex_directory = config["Categorization"]["regular_expression_directory"]
        self.check_file = config["Categorization"].getboolean("check_file")

    def resolve_pars(self, args: argparse.Namespace):  # noqa: C901
        if args.filter_files:
            self.filter_files = True
        if args.filter_directories:
            self.filter_directories = True
        if args.filter_hidden:
            self.filter_hidden = True
        if args.filter_custom is not None:
            self.filter_custom = True
            self.filter_custom_list = args.filter_custom
        if self.filter_custom:
            self.filter_custom_list = self.filter_custom_list.split(",")
        if args.file_count or self.file_count:
            self.file_count = True
            self.measures.append("file_count")
        if args.dir_count or self.dir_count:
            self.dir_count = True
            self.measures.append("dir_count")
        if args.file_size or self.file_size:
            self.file_size = True
            self.measures.append("file_size")
            if args.size_rounding is not None:
                self.file_size_rounding_percentage = args.size_rounding
        if args.modified_time or self.modified_time:
            self.modified_time = True
            self.measures.append("modified_time")
            if args.time_round is not None:
                self.modified_time_rounding_margin = args.time_round
        # to do outputs
        if args.summary:
            self.create_summary = True
        if args.tree:
            self.create_tree = True
        if args.csv:
            self.create_csv = True
        if args.pipe_data:
            self.pipe_data = True
        if args.get_configurations:
            self.get_configurations = True
        if args.target_depth is not None:
            self.target_depth = args.target_depth
        if args.depth_range is not None:
            self.use_depth_range = True
            self.range_start = args.depth_range[0]
            self.range_end = args.depth_range[1]
        if args.depth_limit is not None:
            self.limit_depth = True
            self.depth_limit = args.depth_limit
        if args.log is not None:
            self.log_path = args.log
        if args.log_level is not None:
            self.log_level = args.log_level
        if args.verbose is not None:
            self.verbose = args.verbose
        if args.debug is not None:
            self.debug = args.debug
        if args.root is not None:
            self.root_path = args.root
        if args.file_tree is not None:
            self.file_tree_path = args.file_tree
        else:
            cwd = Path.cwd()
            self.file_tree_path = cwd / self.file_tree_path
