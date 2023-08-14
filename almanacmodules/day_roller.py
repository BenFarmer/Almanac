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
import sqlite3

# PERSONAL
from almanacmodules.weather import RegionalWeather
from almanacmodules.event_coordinator import EventCoordinator
from almanacmodules.location_assembler import LocationAssembler
from almanacmodules.master_timer import MasterTimer
from almanacmodules.get_sheets import MasterConfig


class DayRoller:
    def __init__(self, args, time):
        """DayRoller's job is to index through each day in the year for each of the 100
            biomes within a selected country (country_select).
        DayRoller does not output anything directly to a log.
        DayRoller does not decide if an event happens,
            that is the job of decider.
        DayRoller does not gather the location information of the selected_country,
            that is the job of LocationInfo.
        DayRoller tracks and stores (potentially a config from LocationInfo) the
            day_num, the season_num(and season_name)."""
        self.args = args
        self.time = time

        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.biome_config = master_config.biome_config_master

        self._get_country_id()  # should be handeled by an arg_dict maker
        self._create_sqlite_tables()

        location_assembler = LocationAssembler(
            self.args["location_info"]["location_id"]
        )
        self.indv_biomes_config = location_assembler.indv_model_maker()
        self.master_timer = MasterTimer()  # start the master_timer

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
        for self.time["day_num"] in range(
            self.args["year_info"]["max_day"]
        ):  # daily index

            self._season_updater()
            RegionalWeather(
                self.args, self.time, self.indv_biomes_config
            )  # determines regional weather and loads into SQLITE DB
            EventCoordinator(self.args, self.time, self.indv_biomes_config)
        # master timer is run outside of loop after it is completed
        self.master_timer.update()

    def _create_sqlite_tables(self):
        c = sqlite3.connect(r"/home/ben/Envs/databases/sqlite/Almanac.db")
        regional_weather = """CREATE TABLE IF NOT EXISTS regional_weather (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precipitation BOOL NOT NULL, severity INTEGER NOT NULL, duration INTEGER NOT NULL, weight INTEGER NOT NULL, precip_event BOOL NOT NULL)"""
        natural_events = """CREATE TABLE IF NOT EXISTS natural_events (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, event_name STRING NOT NULL, severity INTEGER NOT NULL, event_description STRING NOT NULL)"""
        astral_events = """CREATE TABLE IF NOT EXISTS astral_events (day_num INTEGER NOT NULL, season STRING NOT NULL, astral_name STRING NOT NULL, astral_type STRING NOT NULL, event_description STRING NOT NULL)"""
        master_timeline = """CREATE TABLE IF NOT EXISTS master_timeline (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precip_event BOOL NOT NULL, astral_event STRING NOT NULL, natural_event STRING NOT NULL)"""
        delete_old_regional_weather = """DELETE FROM regional_weather"""
        delete_old_master_timeline = """DELETE FROM master_timeline"""
        delete_old_natural_events = """DELETE FROM natural_events"""
        delete_old_astral_events = """DELETE FROM astral_events"""

        try:
            cursor = c.cursor()
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
            c.commit()

    def _season_updater(self):  # called from day_index
        #        get_array = caller.GetArray()
        #        self.season = get_array.get_seasons(self.season_num)
        num = self.time["season_num"]
        self.time["season_name"] = self.args["year_info"]["seasons"][num]
        if (self.time["day_num"] / self.args["year_info"]["season_length"]) in [
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

    def _get_country_id(
        self,
    ):  # called from __init_, potentially move to get_args main or other module_
        for row, name in enumerate(self.world_config):
            if (
                self.args["location_info"]["location_name"]
                == self.world_config[row].name
            ):
                self.args["location_info"]["location_id"] = self.world_config[row].id
