#!/bin/env python

""" weather.py is responsible for determining the precipitation
    value of every respective region within a selected country
    through a run of Almanac. 
    The occurance of precipitation is based off of a floating
    precipitation chance that is dependent on:
        - time of year (season)
        - regional biome
        - country temp_zone
    The weather data is packaged into a single list and
    relevant information is pushed into both the
    regional_weather and master_timeline table.
"""

# BUILT INS
import math
import random

# THIRD PARTY
import sqlite3

# PERSONAL
from almanacmodules.rarity_calc import PercentileCheck
from almanacmodules.get_sheets import MasterConfig


# these weather configs should potentially be put into a weather cfg
# REGIONAL WEATHER CONSTANTS
BASE_PRECIP_CHANCE = 0

REGION_ID = 0
BIOME_NAME = 1

# precip_chance season variables
SPRING_BASE = 40
SUMMER_BASE = 20
FALL_BASE = 30
WINTER_BASE = 20

# precip_chance biome variables
DESERT_MOD = 5      # // DESERT_MOD
JUNGLE_MOD = 2      # * JUNGLE_MOD
MOUNTAIN_MOD = 1.5  # // MOUNTAIN_MOD
SWAMP_MOD = 2       # * SWAMP_MOD

# precip_chance temp_zone variables
ZONE_1_MOD = 1.25   # // ZONE_MOD
ZONE_5_MOD = 1.25   # // ZONE_MOD
ZONE_3_MOD = 1.5    # * ZONE_MOD

# severity temp_zone variables
ZONE_3_SEVERITY_MOD = 25
ZONE_1_5_SEVERITY_MOD = 15

# weight variables
WEIGHT_MULTIPLE_MOD = 10    # * WEIGHT_MULTIPLE_MOD
WEIGHT_INVERSE = 6          # WEIGHT_INVERSE - SEVERITY


class RegionalWeather:
    def __init__(self, day_num, country_id, season_num, indv_biomes_config):
        """DailyWeather takes the indv biomes built by location assembler and determines
        a local weather event for each group/region.
        This weather event is based on several factors:
                        - biome_name (biome the weather event takes place in)
                        - temp_zone (general temp shift of country 1-5 (cold - hot)
                                        -> from self.world_config[country_id].temp_zone
                        - season (what time of year it is in the world)
                                        -> in ['name', 'id'] format

        HIERARCHY OF VARIABLES:
                1 - season
                2 - temp_zone
                3 - biome"""
        self.day_num = day_num
        self.season_num = season_num
        self.country_id = country_id
        self.indv_biomes_config = indv_biomes_config

        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.percentile = PercentileCheck()

        self.seasons = ("spring", "summer", "fall", "winter") #could maybe get this from an arg package
        self.season = self.seasons[self.season_num]
        self.region_pack = []
        self._get_region_info()
        self.temp_zone = self._get_temp_zone()
        self.precip_event = False # this should just be here to initialize this variable

        self.precip_chance = BASE_PRECIP_CHANCE

        self.weather_pack = []
        # contains: [day_num, region_id, region biome, precipitation, severity, duration, weight, precip_event]
        self._weather()
        self._sqlite()

    def _get_temp_zone(self):
        for country in self.world_config:
            if country.id == self.country_id:
                return country.temp_zone

    def _get_region_info(self):
        # builds a initial pack with region id, then removes duplicates and appends into region pack
        test_pack = []
        for id in self.indv_biomes_config:
            if id.region_id not in test_pack:
                test_pack.append((id.region_id, id.biome_name))
        [self.region_pack.append(x) for x in test_pack if x not in self.region_pack]

    def _weather(self):
        """ weather first pulls a bool from calc_precipitation
            and if True, determines the severity, duration, and weight (impact)
            of the precipitation within each region, appending the weather_pack
            with the relevant information
        """
        for id, num in enumerate(self.region_pack):
            precipitation = self.calc_precipitation(
                id
            )  # returns a bool based on a precip chance value
            if precipitation is False:
                # values for a 'dry' day
                severity = 0
                duration = 1
                weight = 0
            else:
                severity = (
                    self.calc_severity()
                )  # returns 1-5, with extremes having worse weather
                duration = self.calc_duration(
                    severity
                )  # duration baseline is 1, higher severity can be longer
                weight = self.calc_weight(severity)  # returns a weight (impact) score (0 - 100)
            self.weather_pack.append(
                (
                    self.day_num,
                    self.season,
                    self.region_pack[id][REGION_ID],
                    self.region_pack[id][BIOME_NAME],
                    precipitation,
                    severity,
                    duration,
                    weight,
                    self.precip_event,
                )
            )

    def calc_precipitation(self, id):
        """ this function takes the base precipitation chance from
            a constant variable, and then adjusts it through 3
            different modifiers:
                - seasonal changes
                - biome dependant changes
                - temp_zone changes
            it then takes the final resulting precip_chance and uses it
            as the threshhold for a precip_event, returning true if
            a generated number is below the precip_chance.
        """
        def seasonal_changes():
            if self.season == "summer":
                self.precip_chance = SUMMER_BASE
            elif self.season == "winter":
                self.precip_chance = WINTER_BASE
            elif self.season == "spring":
                self.precip_chance = SPRING_BASE
            else:
                self.precip_chance = FALL_BASE

        def biome_changes():
            biome = self.region_pack[id][BIOME_NAME]
            # forest, plains, desert, swamp, jungle, mountain, lake, river, beach
            if biome == "desert":
                mod = self.precip_chance // DESERT_MOD
                self.precip_chance = mod
            elif biome == "mountain":
                mod = self.precip_chance // MOUNTAIN_MOD
                self.precip_chance = mod
            elif biome == "jungle":
                mod = self.precip_chance * JUNGLE_MOD
                self.precip_chance = mod
            elif biome == "swamp":
                mod = self.precip_chance * SWAMP_MOD
                self.precip_chance = mod

        def temp_changes():
            temp_zone = self.world_config[self.country_id].temp_zone
            if temp_zone == 1:
                mod = self.precip_chance // ZONE_1_MOD
                self.precip_chance = mod
            elif temp_zone == 5:
                mod = self.precip_chance // ZONE_5_MOD
                self.precip_chance = mod
            elif temp_zone == 3:
                mod = self.precip_chance * ZONE_3_MOD
                self.precip_chance = mod

        seasonal_changes()
        biome_changes()
        temp_changes()

        if random.randint(0, 100) <= self.precip_chance:
            return True
        else:
            return False

    def calc_severity(self):
        temp_zone = self.world_config[self.country_id].temp_zone
        severity = self.percentile.norm_rarity()
        if severity == 1:
            return severity
        else:
            if temp_zone == 3:
                if random.randint(0, 100) <= ZONE_3_SEVERITY_MOD:
                    return severity - 1
                else:
                    return severity
            elif temp_zone == 1 or temp_zone == 5:
                if random.randint(0, 100) <= ZONE_1_5_SEVERITY_MOD:
                    return severity - 1
                else:
                    return severity
            else:
                return severity

    def calc_duration(self, severity):
        # baseline duration = 1 day
        if severity == 1:
            return 1 + random.randint(0, 2)
        return 1 + random.randint(0, 1)

    def calc_weight(self, severity):
        # this is a separate function in case this expands later
        weight = (WEIGHT_INVERSE - severity) * WEIGHT_MULTIPLE_MOD
        return weight

    def _sqlite(self):
        conn = sqlite3.connect(r"/home/ben/Envs/databases/sqlite/Almanac.db")
        cursor = conn.cursor()

        for item in self.weather_pack:
            day_num = item[0]
            season = item[1]
            region_id = item[2]
            biome_name = item[3]
            precipitation = item[4]
            severity = item[5]
            duration = item[6]
            weight = item[7]
            precip_event = item[8]

            astral_event = None
            natural_event = None

            insert_regional_weather = (f
                    """INSERT INTO regional_weather (
                        day_num, season, region_id, biome_name, precipitation,
                        severity, duration, weight, precip_event
                        )
                    VALUES (
                        {day_num}, '{season}', {region_id}, '{biome_name}', {precipitation},
                        {severity}, {duration}, {weight}, {precip_event}
                        )
                    """
            insert_master_timeline = (f
                    """INSERT INTO master_timeline (
                        day_num, season, region_id, biome_name,
                        precip_event, astral_event, natural_event
                        )
                    VALUES (
                        {day_num}, '{season}', {region_id}, '{biome_name}',
                        {precip_event}, '{astral_event}', '{natural_event}'
                        )
                    """

            cursor.execute(insert_regional_weather)
            cursor.execute(insert_master_timeline)
        conn.commit()
