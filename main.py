#!/bin/env python

# BUILT-INS
import argparse
import logging  # need to implement
import yaml  # need to implement

# THIRD PARTY
from rich import print as rprint
from rich import pretty

# PERSONAL
from almanacmodules import get_sheets
from almanacmodules.log_write import LogReset
from almanacmodules.day_roller import DayRoller


def main():
    input_country = get_args()
    master_config = get_config()
    country_validator(input_country, master_config)


def country_validator(input_country, master_config):
    accepted_countries = []
    for row in master_config.world_config_master:
        if row.name not in accepted_countries:
            accepted_countries.append(row.name)

    if input_country in accepted_countries:
        start_day_index(input_country)
    else:
        rprint("[red]This country doesn't exist in my library of accepted countries")
        if input("Would you like to try again? y/n: ") == "y":
            input_country = input("Please type the country name again: ")
            country_validator(input_country, master_config)


def start_day_index(input_country):
    day_roller = DayRoller(input_country)
    day_roller.day_index()


def get_config():
    get_config = get_sheets.SheetConversion()
    (
        world_config,
        monster_config,
        biome_config,
        astral_config,
        natural_config,
        effects_config,
    ) = get_config.configs

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_country",
        required=True,
        help="this requires the name of a country",
    )
    parser.add_argument(
        "-r", "--log_reset", default=["n"], choices=["y", "n"], help="(y)es or (n)o"
    )
    parser.add_argument(
        "-l",
        "--logging_level",
        default=["critical"],
        choices=["debug", "info", "warning", "error", "critical"],
        help="sets the logging level of Almanac",
    )

    args = parser.parse_args()

    if args.log_reset == "y":
        rprint("[blue]resetting logs")
        LogReset()

    return args.input_country


if __name__ == "__main__":
    main()
