#!/bin/env python

# long-help
""" Almanac: comprehensive world-building utility to be used in conjunction
    with a role-playing system or just for your own amusement.
    ALmanac creates a yearly report of happenings and events within your
    custom world including:
        - natural disasters such as:
                - earthquakes
                - floods
                - blizards
        - local weather events (that may lead to natural disasters)
        - the fallout of weather and natural events on the local population

    All within a custom world of your design, fully customizable with your
    own monsters, events, and even weather.

    REQUIRED ARGUMENTS:
        -i --input_country          name of the location that you would
                                    like Almanac to use in its yearly run

    OPTIONAL ARGUMENTS:
        --logging_level             sets the logging level of Almanac
                                    (Default: CRITICAL)
        -d --delete_logs            deletes prior logs

    FUTURE LOGS (to be implemented next package)
        -l --logs                   specifies how logs are saved
        -r --run_times              specifies how many times (years) Almanac will run
                                    (Default: 1)
"""

# BUILT-INS
import argparse
import logging
import yaml

# THIRD PARTY
from rich import print as rprint

# from rich import pretty
from rich.logging import RichHandler

# PERSONAL
from almanacmodules import get_sheets
from almanacmodules.log_write import LogReset
from almanacmodules.day_roller import DayRoller


def main():
    args, time = get_args()
    master_config = get_config()
    country_validator(args, time, master_config)


def country_validator(args, time, master_config):
    """validates that the input country exists within the
    master_config and if it fails, re-runs the validator
    with a new input country.
    """
    accepted_countries = []
    for row in master_config.world_config_master:
        if row.name not in accepted_countries:
            accepted_countries.append(row.name)

    if args["location_info"]["location_name"] in accepted_countries:
        logging.info(
            f"[bold red]input_country validated: {args['location_info']['location_name']}"
        )
        start_day_index(args, time)
    else:
        rprint("[red]This country doesn't exist in my library of accepted countries")
        if input("Would you like to try again? y/n: ") == "y":
            args["location_info"]["location_name"] = input(
                "Please input the country name again: "
            )
            country_validator(args, time, master_config)


def start_day_index(args, time):
    """this starts the yearly run of Almanac and is called only after
    the input country is properly validated against the master_config
    """
    day_roller = DayRoller(args, time)
    day_roller.day_index()


def get_config():
    """Almanac uses several configs of information that are gathered through
    several different processes. The most important config is master_config
    which is made up different pydantic classes.
    """
    sheets = get_sheets.SheetConversion()
    (
        world_config,
        monster_config,
        biome_config,
        astral_config,
        natural_config,
        effects_config,
    ) = sheets.configs

    master_config = get_sheets.MasterConfig()
    master_config.append_configs(
        world_config,
        monster_config,
        biome_config,
        astral_config,
        natural_config,
        effects_config,
    )
    return master_config


def get_args():
    """pieces together the passed arguments into a single dictionary
    that can be referenced through Almanac when needed.
    get_args also sets the logging level of Almanac.
    """

    def get_yaml():
        with open("config.yaml") as stream:
            try:
                yaml_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.critical(exc)
            finally:
                return yaml_config

    def build_arg_dict(input_country, yaml_config):
        arg_dict = {
            "location_info": {
                "location_name": input_country,
                "location_id": None,
                "temp_zone": None,
            },
            "year_info": {
                "seasons": yaml_config["seasons"],
                "start_day": yaml_config["start_day"],
                "max_day": yaml_config["max_day"],
                "months_in_year": yaml_config["months_in_year"],
                "season_length": yaml_config["season_length"],
                "month_length": yaml_config["month_length"],
            },
            "event": {
                "rand_event_chance": yaml_config["rand_event_chance"],
                "event_names": yaml_config["event_names"],
            },
            "weather_constants": {
                "base_precip_chance": yaml_config["base_precip_chance"],
            },
        }
        return arg_dict

    def build_time_dict(yaml_config):
        num = yaml_config["season_num_start"]
        time = {
            "day_num": yaml_config["start_day"],
            "season_num": yaml_config["season_num_start"],
            "season_name": yaml_config["seasons"][num],
        }
        return time

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_country",
        required=True,
        help="requires the name of a recognized country",
    )
    parser.add_argument(
        "-d",
        "--delete_logs",
        default=["n"],
        choices=["y", "n"],
        help="a value of 'y' will delete all created logs prior to this run of Almanac",
    )
    parser.add_argument(
        "--logging_level",
        default="warning",
        choices=["debug", "info", "warning", "error", "critical"],
        help="sets the logging level of Almanac",
    )

    args = parser.parse_args()
    setup_logging(args.logging_level)
    logging.debug(args)

    if args.delete_logs == "y":
        logging.info("[bold red] Resetting logs")
        LogReset()

    yaml_config = get_yaml()
    arg_dict = build_arg_dict(args.input_country, yaml_config)
    time_dict = build_time_dict(yaml_config)
    logging.info(f"[bold red]arg_dict:[/] {arg_dict}")
    return arg_dict, time_dict


def setup_logging(logging_level):
    log_level = str(logging_level).upper()
    rprint(f"[bold red blink]Current Log Level: {log_level}")

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.getLevelName(log_level),
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
    )


if __name__ == "__main__":
    main()
