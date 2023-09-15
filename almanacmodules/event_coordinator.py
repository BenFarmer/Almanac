#!/bin/env python

""" event_coordinator also determines if a likely or random event will attempt to occur.
    Any astral or natural event that does attempt to occur will be inserted into
    their respective table to be verified later by master timer.
"""


# BUILT IN
import random

# THIRD PARTY

# PERSONAL
from almanacmodules.astral import AstralInfo
from almanacmodules.natural import NaturalInfo

# LIKELY EVENT CONSTANTS
DAYS_PAST = 7  # how many prior days are looked at for scoring
REGION_ID = 2

# past_weather list variables
DAY_NUM = 0
YEAR = 1
SEASON = 2
REGION_ID = 3
BIOME_NAME = 4
WEIGHT = 8

# score math variables
SCORE_START = 0
WEATHER_WEIGHT = 5
SCORE_LIMIT = 190

# RANDOM EVENT CONSTANTS
LOCATION = 0
EVENT = 1
SEVERITY = 2


class LikelyEvent:
    """this takes the precipitation score of each region and decides whether or not
    precipitation occurs in that region. If precipitation does occur, then this
    updates both regional_weather and master_timeline tables with that information.
    This needs to then:
        - communicate with prereqs module to see if precipitation causes any events
    """

    def __init__(self, args, time, conn):
        self.args = args
        self.time = time
        self.cursor = conn.cursor()

        self.year = self.time["year"]
        self.day_num = self.time["day_num"]
        self.season_name = self.time["season_name"]
        self.location_id = self.args["location_info"]["location_id"]
        self.past_date = self.day_num - DAYS_PAST
        self.cursor = conn.cursor()

        self.check_precip_value()

    def check_precip_value(self):
        # needs to get precip value
        # needs to check prereqs to see if precip value can cause anything
        # will attempt to do that
        # will insert the new precip related event into natural events
        query = self.cursor.execute(
            f"""
            SELECT precip_value, biome_name
            FROM regional_weather
            WHERE day_num = {self.day_num}
            AND year = {self.year}
            """
        )
        for result in query:
            rslt = []
            rslt.append(result)


class RandomEvent:
    def __init__(self, args, time, indv_biomes_config, conn):
        """LargeEvent handles the decisions needed to piece together a large scale event.
        These events generally have country-wide implications, but also can have small
        scale effects as well."""
        self.args = args
        self.time = time
        self.conn = conn

        self.day_num = self.time["day_num"]
        self.season_name = self.time["season_name"]
        self.location_id = self.args["location_info"]["location_id"]
        self.indv_biomes_config = indv_biomes_config
        self.event_details = None
        self.cursor = conn.cursor()

    def event(self):
        pick = random.randint(0, len(self.args["event"]["event_names"]) - 1)
        event_type = self.args["event"]["event_names"][pick]

        if event_type == "astral":
            astral_info = AstralInfo()
            self.event_details = astral_info.get_astral()

            astral_name = self.event_details[0][1]
            astral_type = self.event_details[0][2]
            event_description = self.event_details[0][3]
            input_astral = f"""
                INSERT INTO astral_events
                    (day_num, year, season, astral_name, astral_type, event_description)
                VALUES
                    ({self.day_num}, {self.time["year"]}, '{self.season_name}', '{astral_name}',
                    '{astral_type}', '{event_description}')
                """
            self.cursor.execute(input_astral)
            self.conn.commit()
            # [(61, 'Helene', 'moon', 'has eclipsed the sun,')]

        elif event_type == "natural":
            natural_info = NaturalInfo(self.args["location_info"]["location_id"])
            natural_info.load_config()
            self.event_details = natural_info.decide_natural(self.indv_biomes_config)
            events = []
            # this works but natural is only returning 1 event for each day
            for event in self.event_details:
                region_id = event[LOCATION].indv_id
                biome_name = event[LOCATION].biome_name
                event_name = event[EVENT]
                severity = event[SEVERITY]
                event_description = None
                events.append(
                    (region_id, biome_name, event_name, severity, event_description)
                )

            for event in events:
                region_id = event[0]
                biome_name = event[1]
                event_name = event[2]
                severity = event[3]
                event_description = event[4]
                input_natural = f"""
                    INSERT INTO natural_events
                        (day_num, year, season, region_id, biome_name, event_name, severity, event_description)
                    VALUES
                        ({self.day_num}, {self.time["year"]}, '{self.season_name}', {region_id}, '{biome_name}',
                        '{event_name}',{severity}, '{event_description}')
                    """
                self.cursor.execute(input_natural)
                self.conn.commit()

            # [(IndvBiome(indv_id=56, biome_name='swamp', cell_position_x=2, cell_position_y=0,
            #    region_id=21), ('sinkhole', 'thunderstorm')]


class EventCoordinator:
    def __init__(self, args, time, indv_biomes_config, conn):
        """EventCoordinator has a few important responsibilities.
        1 - reference SQLite reader and a prerequisites module to determine if there are any
            events (large/major/global or small/minor/local) that *should* happen.
        2 - determine if an event tries happens randomly, then gather the details of that event
            from whatever module is necessary, then send that information into the correct table.
        """
        self.args = args
        self.time = time
        self.conn = conn

        self.day_num = self.time["day_num"]
        self.location_id = self.args["location_info"]["location_id"]
        self.season_num = self.time["season_num"]
        self.indv_biomes_config = indv_biomes_config

        self.cursor = conn.cursor()
        self._event_determiner()

    def _event_determiner(self):
        LikelyEvent(self.args, self.time, self.conn)
        random_event = RandomEvent(
            self.args, self.time, self.indv_biomes_config, self.conn
        )

        def _random_check():
            if random.randint(0, 100) < self.args["event"]["rand_event_chance"]:
                random_event.event()

        _random_check()
