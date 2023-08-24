#!/bin/env python

# BUILT INS
import argparse
import yaml
import logging

# THIRD PARTY
from rich import print as rprint
from rich.logging import RichHandler

# PERSONAL
from almanacmodules.log_write import LogReset


class GetArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None
        self._parsed_arguments()

        self.yaml_config = self._get_yaml()
        self.arg_dict = self._build_arg_dict()
        self.time_dict = self._build_time_dict()

#        self._setup_logging()


    def _parsed_arguments(self):
        # REQUIRED ARGUMENTS
        self.parser.add_argument(
            "-i",
            "--input_location",
            required=True,
            help="name of a recognized location that Almanac will produce a timeline for",
        )

        # OPTIONAL ARGUMENTS
        self.parser.add_argument(
            "-d",
            "--delete_logs",
            choices=["y", "n"],
            help="option to delete previous Almanac dev and user logs",
        )

        self.parser.add_argument(
            "--logging_level",
            default="warning",
            choices=["debug", "info", "warning", "error", "critical"],
            help="sets the logging level of Almanac",
        )

        self.parser.add_argument(
            "-r",
            "--report",
            choices=['y','n'],
            help="option to run reporting on currenct Almanac run",
        )

        self.args = self.parser.parse_args()

        if self.args.delete_logs == "y":
            logging.info("[bold red blink] Resetting Logs")
            LogReset()

    def _get_yaml(self):
        with open("config.yaml") as stream:
            try:
                yaml_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.critical(exc)
            finally:
                return yaml_config

    def _build_arg_dict(self):
        def _get_location_id():
            return None
        def _get_temp_zone():
            return None
        arg_dict = {
            "location_info": {
                "location_name": self.args.input_location,
                "location_id": _get_location_id(),
                "temp_zone": _get_temp_zone(),
            },
            "year_info": {
                "year_num": self.yaml_config["year_num"],
                "seasons": self.yaml_config["seasons"],
                "start_day": self.yaml_config["start_day"],
                "max_day": self.yaml_config["max_day"],
                "months_in_year": self.yaml_config["months_in_year"],
                "season_length": self.yaml_config["season_length"],
                "month_length": self.yaml_config["month_length"],
            },
            "event": {
                "rand_event_chance": self.yaml_config["rand_event_chance"],
                "event_names": self.yaml_config["event_names"],
            },
            "weather_constants": {
                "base_precip_chance": self.yaml_config["base_precip_chance"],
            },
            "log_level": self.args.logging_level,
            "report": self.args.report,
        }
        return arg_dict

    def _build_time_dict(self):
        time = {
            "day_num": self.yaml_config["start_day"],
            "season_num": self.yaml_config["season_num_start"],
            "season_name": self.yaml_config["seasons"][(self.yaml_config["season_num_start"])],
        }
        return time

    def _setup_logging(self):
        log_level = str(self.args.logging_level).upper()
        rprint(f"[bold red blink]Current Log Level: {log_level}")

        FORMAT = "%(message)s"
        logging.basicConfig(
                level=logging.getLevelName(log_level),
                format=FORMAT,
                datefmt="[%X]",
                handlers=[RichHandler(markup=True)],
        )

    def dicts(self):
        logging.info(f"[bold red]Input Arguments:[/] {self.args}")
        logging.info(f"[bold red]arg_dict:[/] {self.arg_dict}")
        return self.arg_dict, self.time_dict
