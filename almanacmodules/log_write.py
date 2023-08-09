#!/bin/env python
# user_log_write.py

import csv
from pathlib import Path
import os


class LogReset:
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
    def __init__(self, output):
        self.output = output

    def user_log_write(self):
        #    csv.writer(csvfile, dialect='excel', **fmtparams)
        with open("userlog.csv", "a", newline="") as file:
            writer = csv.writer(file)
            header = ("day num", "output")
            writer.writerow([self.output])


class DevLogWrite:
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
