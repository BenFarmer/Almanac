#!/bin/env python

# BUILT INS
import logging

# THIRD PARTY

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

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.astral_events = []
        self.natural_events = []

    def update(self):
        def fetch_astral():
            fetch_astral_events = "SELECT * FROM astral_events;"
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
            logging.debug(
                f"""
                [bold red]Astral Events PRE-VALIDATION:[/]
                DAY NUM 0, SEASON 1, ASTRAL NAME 2, ASTRAL TYPE 3, ASTRAL DESCRIPTION 4
                {self.astral_events}"""
            )

        def fetch_natural():
            fetch_natural_events = "SELECT * FROM natural_events;"
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
            logging.debug(
                f"""
                [bold red] Natural Events PRE-VALIDATION:[/]
                DAY NUM 0, SEASON 1, REGION_ID 2, BIOME_NAME 3, EVENT_NAME 4, NATURAL_DESCRIPTION 5
                {self.natural_events}"""
            )

        fetch_astral()
        fetch_natural()
        self._finalize_events()

    def _finalize_events(self):  # should consider renaming to 'validate_events'
        """finalize_events takes the events that are attempting to happen
        and double checks their conditions against the event_prereqs models.
        if they pass this testing, they are pushed into the master_timeline.
        """

        def verify_astral():
            logging.info("verifying_astral")

        def verify_natural():
            for event in self.natural_events:
                if event[5] == "None":
                    logging.warning("event description seems to be missing here")
                else:
                    logging.info("start validation of events against event_prereqs")

        def event_duration():
            logging.info("verifying_astral")

        verify_astral()
        verify_natural()
        event_duration()


# class UpdateDuration:
#    def __init__(self):
