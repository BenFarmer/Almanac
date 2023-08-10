#!/bin/env python

""" log_write handles the output and creation of both a userlog and devlog.
    currently both of these logs are created as csv files within the 
    folder that contains the sqlite database.
"""

# BUILT INS
import csv
from pathlib import Path
import os


class LogReset:
    """ checks for both a userlog.csv and devlog.csv and
        if exists removes them.
    """
    def __init__(self):
        self.log_reset()

    def log_reset(self):
        checked_file = Path("userlog.csv")
        if checked_file.is_file():
            checked_file.unlink()

        checked_file = Path("/home/ben/Envs/databases/devlog.csv")
        if checked_file.is_file():
            checked_file.unlink()


class UserLogWrite:
    """ writes to a userlog.csv information about what is happening
        on each day within Almanac. This may potentially become more
        useful in the future, but in the meantime querying the sqlite
        tables such as master_timeline is much easier and holds more information.
    """
    def __init__(self, output):
        self.output = output

    def user_log_write(self):
        #    csv.writer(csvfile, dialect='excel', **fmtparams)
        with open("userlog.csv", "a", newline="") as file:
            writer = csv.writer(file)
            header = ("day num", "output")
            writer.writerow([self.output])


class DevLogWrite:
    """ writes to a devlog.csv important information in regards
        to the running of Almanac. Similarly to the userlog.csv,
        this information is more easily accessed through logs and
        querying the sqlite database directly.
    """
    def __init__(self, dev_log_astral, dev_log_natural):
        self.dev_log_astral = dev_log_astral
        self.dev_log_natural = dev_log_natural

    ########## UNUSED ########
    def write_headers(self):
        with open(
            "/home/ben/Envs/databases/devlog_astral.csv", "a", newline=""
        ) as file:
            writer = csv.writer(file)
            header = (
                "day_num",
                "event_type",
                "biome_id",
                "monster_name",
                "rand_astral",
                "astral_pick",
                "p_event_pick",
                "m_event_pick",
            )

    def write_log_astral(self):
        with open(
            "/home/ben/Envs/databases/devlog_astral.csv", "a", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([self.dev_log_astral])

    def write_log_natural(self):
        with open(
            "/home/ben/Envs/databases/devlog_natural.csv", "a", newline=""
        ) as file:
            writer = csv.writer(file)
            #            header = (
            #                "day_num",
            #                "event_type",
            #                "biome_name",
            #                "country_id",
            #                "last_name",
            #            )
            #            writer.writerow([header])
            writer.writerow([self.dev_log_natural])
