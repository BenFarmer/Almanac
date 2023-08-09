#!/bin/env python

import sqlite3
from pydantic import BaseModel

c = sqlite3.connect(r"/home/ben/Envs/databases/sqlite/Almanac.db")

# CONSTANTS
DAY_NUM = 0
SEASON = 1
ASTRAL_NAME = 2
ASTRAL_TYPE = 3
ASTRAL_DESCRIPTION = 4

REGION_ID = 2
BIOME_NAME = 3
EVENT_NAME = 4
NATURAL_DESCRIPTION = 5


class MasterTimer:
    """This class is the primary control for the timing of events and their effects.
    For example, when as astral event causes a monstrous effect, this controls the
    timing for how long that effect lasts for.
    """

    def __init__(self):
        self.cursor = c.cursor()

        self.astral_events = []
        self.natural_events = []

    def update(self):
        def fetch_astral():
            fetch_astral_events = f"SELECT * FROM astral_events;"
            self.cursor.execute(fetch_astral_events)
            rows = self.cursor.fetchall()
            for row in rows:
                self.astral_events.append(
                    (
                        row[DAY_NUM],
                        row[SEASON],
                        row[ASTRAL_NAME],
                        row[ASTRAL_TYPE],
                        row[ASTRAL_DESCRIPTION],
                    )
                )

        def fetch_natural():
            fetch_natural_events = f"SELECT * FROM natural_events;"
            self.cursor.execute(fetch_natural_events)
            rows = self.cursor.fetchall()
            for row in rows:
                self.natural_events.append(
                    (
                        row[DAY_NUM],
                        row[SEASON],
                        row[REGION_ID],
                        row[BIOME_NAME],
                        row[EVENT_NAME],
                        row[NATURAL_DESCRIPTION],
                    )
                )

        fetch_astral()
        fetch_natural()
        self._finalize_events()

    def _finalize_events(self):
        def verify_astral():
            place_holder = True

        def verify_natural():
            for event in self.natural_events:
                if event[5] == "None":
                    print(
                        "this needs to double check that the event description exists just in case -- MasterTimer"
                    )
                else:
                    print(
                        "then if everything is ready, checks against params for if event makes sense -- MasterTimer"
                    )

        def event_duration():
            placeholder = False

        verify_astral()
        verify_natural()
        event_duration()


# class UpdateDuration:
#    def __init__(self):
