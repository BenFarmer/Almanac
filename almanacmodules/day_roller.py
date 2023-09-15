#!/bin/env python

""" The majority of Almanacs function is controlled from this module.
    day_roller 'rolls' through each day within a year
    day_roller also creates all of the required sqlite tables:
        - master_timeline
        - regional_weather
        - astral_events
        - natural_events
"""

# BUILT INS
import logging

# THIRD PARTY

# PERSONAL
from almanacmodules.weather import RegionalWeather
from almanacmodules.event_coordinator import EventCoordinator
from almanacmodules.location_assembler import LocationAssembler
from almanacmodules.master_timer import MasterTimer
from almanacmodules.get_sheets import MasterConfig


class DayRoller:
    def __init__(self, args, time, conn):
        """DayRoller's job is to index through each day in the year for each of the
            biomes within a selected location.
        DayRoller does not output anything directly to a log.
        DayRoller does not decide if an event happens.
        DayRoller does not gather the location information of the selected_country,
            that is the job of LocationInfo.
        """
        self.args = args
        self.time = time
        self.conn = conn

        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.biome_config = master_config.biome_config_master

        self._create_sqlite_tables()

        location_assembler = LocationAssembler(
            self.args["location_info"]["location_id"]
        )
        self.indv_biomes_config = location_assembler.indv_model_maker()
        self.master_timer = MasterTimer(conn)  # start the master_timer

    def day_index(self):
        """indexes through each day, calling the daily_biome_index, and a decider type
        function that determines if an astral or natural event happens.
        STEP 1 - OPEN CONNECTION TO SQLITE
        STEP 2 - UPDATES SEASON
        STEP 3 - RUN DAILY WEATHER
                    |-> DETERMINE REGIONAL WEATHER FOR EACH REGION IN INDV_BIOME_CONFIG
                    |-> LOAD REGIONAL WEATHER TO SQLITE DB TABLE 'regional_weather'
        STEP 4 - RUN EVENT COORD.
                    |-> DETERMINE LIKELY/RANDOM EVENTS
                        |-> DETERMINE FALLOUT AND DURATION
                    |-> CHECK WITH MASTER TIMER IF ANY EVENTS END
                    |-> VALIDATE EVENTS CAN HAPPEN -> READ SQLITE DB
                    |-> RETURN DAILY EVENT BUNDLE
                            |-> LIKELY/RANDOM/ENDING EVENTS
        STEP 5 - SEND DAILY EVENT BUNDLE TO OUTPUT MANAGER
        """
        logging.info("[bold red]day_index started")
        for year in range(self.args["system"]["run_times"]):
            logging.info(f"current year: {self.time['year']}")
            for self.time["day_num"] in range(
                self.args["year_info"]["max_day"]
            ):  # daily index
                self._season_updater()
                RegionalWeather(
                    self.args, self.time, self.indv_biomes_config, self.conn
                )  # determines regional weather and loads into SQLITE DB
                EventCoordinator(
                    self.args, self.time, self.indv_biomes_config, self.conn
                )

            # this segment here is to update to the next year but also
            # double checks that every year is starting on the correct day/season
            # this needs to be worked so it just copies a clean snapshot of the original
            # starting state of Almanac
            self.time["year"] += 1
            self.time["day_num"] = 1
            self.time["season_num"] = 0
            self.time["season_name"] = "spring"
        self.master_timer.update()

    def _create_sqlite_tables(self):
        regional_weather = """CREATE TABLE IF NOT EXISTS regional_weather (day_num INTEGER NOT NULL, year INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precipitation BOOL NOT NULL, severity INTEGER NOT NULL, duration INTEGER NOT NULL, precip_value INTEGER NOT NULL, precip_event BOOL NOT NULL)"""
        natural_events = """CREATE TABLE IF NOT EXISTS natural_events (day_num INTEGER NOT NULL, year INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, event_name STRING NOT NULL, severity INTEGER NOT NULL, event_description STRING NOT NULL)"""
        astral_events = """CREATE TABLE IF NOT EXISTS astral_events (day_num INTEGER NOT NULL, year INTEGER NOT NULL, season STRING NOT NULL, astral_name STRING NOT NULL, astral_type STRING NOT NULL, event_description STRING NOT NULL)"""
        master_timeline = """CREATE TABLE IF NOT EXISTS master_timeline (day_num INTEGER NOT NULL, year INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precip_event BOOL NOT NULL, astral_event STRING NOT NULL, natural_event STRING NOT NULL)"""
        delete_old_regional_weather = """DELETE FROM regional_weather"""
        delete_old_master_timeline = """DELETE FROM master_timeline"""
        delete_old_natural_events = """DELETE FROM natural_events"""
        delete_old_astral_events = """DELETE FROM astral_events"""

        try:
            cursor = self.conn.cursor()
            cursor.execute(regional_weather)
            cursor.execute(master_timeline)
            cursor.execute(natural_events)
            cursor.execute(astral_events)
            cursor.execute(delete_old_regional_weather)
            cursor.execute(delete_old_master_timeline)
            cursor.execute(delete_old_natural_events)
            cursor.execute(delete_old_astral_events)
            logging.info("[bold red]sqlite tables created")
        except ConnectionError as e:
            logging.critical(e)
        finally:
            self.conn.commit()

    def _season_updater(self):  # called from day_index
        num = self.time["season_num"]
        day = self.time["day_num"]
        season_length = self.args["year_info"]["season_length"]
        self.time["season_name"] = self.args["year_info"]["seasons"][num]

        if (day / season_length) in [
            1,
            2,
            3,
            4,
        ]:
            if self.time["season_num"] != 3:
                self.time["season_num"] += 1
                logging.debug(
                    f"[bold red]season updated to:[/] {self.time['season_name']}"
                )
            else:
                logging.debug(
                    f"[bold red]season updated to:[/] {self.time['season_name']}"
                )
