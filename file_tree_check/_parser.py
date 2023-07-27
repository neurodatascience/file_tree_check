from __future__ import annotations

import argparse
import configparser
import logging
import os
from pathlib import Path
from typing import Sequence


class Parser:
    """Class to parse command line arguments and configuration file."""

    DEFAULT_CONFIG_PATH = os.path.join(Path(__file__).parent, "config.ini")

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"file_tree_check.{__name__}")
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
        self.output_dir = None
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
        self.log_path = None
        self.verbose = False
        self.debug = False
        # Input
        self.root_path = None
        self.file_tree_path = None
        # To Be Deprecated
        self.regex_file = ""
        self.regex_directory = ""
        self.check_file = False

    def make_parser(self, config_path: Path | str = None, argv: Sequence[str] | None = None):
        parser = self.pars_args()
        args = parser.parse_args(argv)
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
        parser.add_argument("-c", "--config", type=Path, help="Path to configuration file.")
        parser.add_argument(
            "-r", "--root", type=Path, help="Path to root directory to be explored."
        )
        parser.add_argument("-f", "--file_tree", type=Path, help="Path to file tree to be used.")
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
            type=Path,
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
        parser.add_argument("-l", "--log", type=Path, help="Path to log file.")
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
        self.depth_limit = (
            config["Configurations"].getint("depth_limit") if self.limit_depth else None
        )
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

    def output_handler(
        self,
        output_dir: str,
    ):
        if not Path(output_dir).exists():
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            Path(output_dir).touch()
        if self.summary_path is not None and self.create_summary:
            self.summary_path = os.path.join(output_dir, Path(self.summary_path).name)
        if self.tree_path is not None and self.create_tree:
            self.tree_path = os.path.join(output_dir, Path(self.tree_path).name)
        if self.csv_path is not None and self.create_csv:
            self.csv_path = os.path.join(output_dir, Path(self.csv_path).name)
        if self.log_path is not None:
            self.log_path = os.path.join(output_dir, Path(self.log_path).name)

    def file_tree_handler(
        self,
        tree: str,
    ):
        if ".tree" not in tree.name:
            search_dir = os.path.join(Path(__file__).parent, "trees")
            for child in os.listdir(search_dir):
                if tree.name == child.split(".")[0]:
                    self.file_tree_path = os.path.join(search_dir, child)
                    return
        else:
            self.file_tree_path = tree
            self.logger.info("No default file_tree match found, input file_tree is considered path")

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
            for name in self.filter_custom_list:
                name = name.strip()

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
        if args.output is not None:
            self.output_handler(args.output)
        if args.log_level is not None:
            self.log_level = args.log_level
        if args.verbose is not None:
            self.verbose = args.verbose
        if args.debug is not None:
            self.debug = args.debug
        if args.root is not None:
            self.root_path = args.root
        if args.file_tree is not None:
            self.file_tree_handler(args.file_tree)
        else:
            cwd = Path.cwd()
            self.file_tree_path = cwd / self.file_tree_path
