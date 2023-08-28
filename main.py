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
import logging

# THIRD PARTY
from rich import print as rprint
from rich.logging import RichHandler
import sqlite3

# PERSONAL
from almanacmodules import get_sheets
from almanacmodules.day_roller import DayRoller
from almanacmodules.get_args import GetArguments
from almanacmodules.reporting import Reports


def main():
    get_arguments = GetArguments()
    args, time = get_arguments.dicts()

    setup_logging(args["system"]["log_level"])
    logging.debug(args)

    conn = create_conn()

    master_config = get_config()
    country_validator(args, time, master_config, conn)

    if args["system"]["report"] == "y":
        Reports(master_config, args, time, conn)

    logging.info("[bold red] End of Almanac")


def setup_logging(logging_level):
    log_level = str(logging_level).upper()
    rprint(f"[bold red]Current Log Level:[/][bold red blink] {log_level}")

    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.getLevelName(log_level),
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
    )


def create_conn():
    conn = sqlite3.connect(r"/home/ben/Envs/databases/sqlite/Almanac.db")
    return conn


def country_validator(args, time, master_config, conn):
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
        start_day_index(args, time, conn)
    else:
        rprint("[red]This country doesn't exist in my library of accepted countries")
        if input("Would you like to try again? y/n: ") == "y":
            args["location_info"]["location_name"] = input(
                "Please input the country name again: "
            )
            country_validator(args, time, master_config, conn)


def start_day_index(args, time, conn):
    """this starts the yearly run of Almanac and is called only after
    the input country is properly validated against the master_config
    """
    day_roller = DayRoller(args, time, conn)
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


if __name__ == "__main__":
    main()
