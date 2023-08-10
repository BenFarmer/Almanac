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
import math, random

# THIRD PARTY
import sqlite3

# PERSONAL
from almanacmodules import cfg, caller
from almanacmodules.weather import RegionalWeather
from almanacmodules.event_coordinator import EventCoordinator
from almanacmodules.location_assembler import LocationAssembler
from almanacmodules.master_timer import MasterTimer
from almanacmodules.get_sheets import MasterConfig

# DAY ROLLER CONSTANTS
SEASON_NUM_START = 0  # SPRING
MONTHS_IN_YEAR = 12
MONTHS_IN_SEASON = 3
DAYS_IN_MONTH = 30  # unused atm


class DayRoller:
    def __init__(self, country_select):
        """DayRoller's job is to index through each day in the year for each of the 100
            biomes within a selected country (country_select).
        DayRoller does not output anything directly to a log.
        DayRoller does not decide if an event happens,
            that is the job of decider.
        DayRoller does not gather the location information of the selected_country,
            that is the job of LocationInfo.
        DayRoller tracks and stores (potentially a config from LocationInfo) the
            day_num, the season_num(and season_name)."""

        self._create_sqlite_tables()

        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.biome_config = master_config.biome_config_master

        self.country_select = country_select
        self.country_id = self._get_country_id()

        location_assembler = LocationAssembler(self.country_id)
        self.indv_biomes_config = location_assembler.indv_model_maker()

        self.season_num = SEASON_NUM_START
        self.seasons = ["spring", "summer", "fall", "winter"]
        self.season = None

        self.month_length, self.season_length = self._year_div()
        self.day_num = cfg.start_day  # starts at 1

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
        for self.day_num in range(cfg.max_day):  # daily index
            #            sqlite_control = SQLiteControl
            #            sqlite_control.create_connection
            #            print('sql connection')

            self._season_updater()

            regional_weather = RegionalWeather(
                self.day_num, self.country_id, self.season_num, self.indv_biomes_config
            )  # determines regional weather and loads into SQLITE DB

            event_coordinator = EventCoordinator(
                self.day_num, self.country_id, self.season, self.indv_biomes_config
            )
        # master timer is run outside of loop after it is completed
        self.master_timer.update()

    def _create_sqlite_tables(self):
        c = sqlite3.connect(r"/home/ben/Envs/databases/sqlite/Almanac.db")
        cursor = c.cursor()
        regional_weather = """CREATE TABLE IF NOT EXISTS regional_weather (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precipitation BOOL NOT NULL, severity INTEGER NOT NULL, duration INTEGER NOT NULL, weight INTEGER NOT NULL, precip_event BOOL NOT NULL)"""
        natural_events = """CREATE TABLE IF NOT EXISTS natural_events (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, event_name STRING NOT NULL, severity INTEGER NOT NULL, event_description STRING NOT NULL)"""
        astral_events = """CREATE TABLE IF NOT EXISTS astral_events (day_num INTEGER NOT NULL, season STRING NOT NULL, astral_name STRING NOT NULL, astral_type STRING NOT NULL, event_description STRING NOT NULL)"""
        master_timeline = """CREATE TABLE IF NOT EXISTS master_timeline (day_num INTEGER NOT NULL, season STRING NOT NULL, region_id INTEGER NOT NULL, biome_name STRING NOT NULL, precip_event BOOL NOT NULL, astral_event STRING NOT NULL, natural_event STRING NOT NULL)"""
        delete_old_regional_weather = """DELETE FROM regional_weather"""
        delete_old_master_timeline = """DELETE FROM master_timeline"""
        delete_old_natural_events = """DELETE FROM natural_events"""
        delete_old_astral_events = """DELETE FROM astral_events"""

        cursor.execute(regional_weather)
        cursor.execute(master_timeline)
        cursor.execute(natural_events)
        cursor.execute(astral_events)
        cursor.execute(delete_old_regional_weather)
        cursor.execute(delete_old_master_timeline)
        cursor.execute(delete_old_natural_events)
        cursor.execute(delete_old_astral_events)
        c.commit()

    def _season_updater(self):  # called from day_index
        #        get_array = caller.GetArray()
        #        self.season = get_array.get_seasons(self.season_num)
        self.season = self.seasons[self.season_num]
        if (self.day_num / self.season_length) in [1, 2, 3, 4]:
            if self.season_num == 3:
                self.season_num = self.season_num
            else:
                self.season_num += 1

    def _get_country_id(self):  # called from __init__
        for row, name in enumerate(self.world_config):
            if self.country_select == self.world_config[row].name:
                id = self.world_config[row].id
                return id

    def _year_div(self):  # called from __init__
        """year_div returns the month_length and season_length in days"""
        month_length = round(cfg.max_day / MONTHS_IN_YEAR)
        season_length = month_length * MONTHS_IN_SEASON
        return month_length, season_length
