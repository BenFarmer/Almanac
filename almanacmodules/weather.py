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
import random

# THIRD PARTY

# PERSONAL
from almanacmodules.rarity_calc import PercentileCheck
from almanacmodules.get_sheets import MasterConfig


# these weather configs should potentially be put into a weather cfg
# or into the args dict as a weather sub dict
# REGIONAL WEATHER CONSTANTS
BASE_PRECIP_CHANCE = 0

# LIST LOCATIONS !!!! THIS IS BAD
REGION_ID = 0
BIOME_NAME = 1

# precip_chance season variables
SPRING_BASE = 50
SUMMER_BASE = 10
FALL_BASE = 30
WINTER_BASE = 20

# precip_chance biome variables
DESERT_MOD = 8  # // DESERT_MOD
JUNGLE_MOD = 2  # * JUNGLE_MOD
MOUNTAIN_MOD = 1.5  # // MOUNTAIN_MOD
SWAMP_MOD = 2  # * SWAMP_MOD

# precip_chance temp_zone variables
ZONE_1_MOD = 1.25  # // ZONE_MOD
ZONE_5_MOD = 1.25  # // ZONE_MOD
ZONE_3_MOD = 1.5  # * ZONE_MOD

# severity temp_zone variables
ZONE_3_SEVERITY_MOD = 25
ZONE_1_5_SEVERITY_MOD = 15

# weight variables
WEIGHT_MULTIPLE_MOD = 10  # * WEIGHT_MULTIPLE_MOD
WEIGHT_INVERSE = 6  # WEIGHT_INVERSE - SEVERITY

# constants for new precip system
STARTING_PRECIP_VALUE = 50  # starting value for weight
DRY_WEIGHT_BASE = 0


class RegionalWeather:
    def __init__(self, args, time, indv_biomes_config, conn):
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

        # change weight value in the sqlite db to just a precip value
        # precip value is inherited from each previous day, and starts at
        # somewhere around 50-100 maybe depending on biome
        # each day if there is precip, the value increases by the weight of the precip
        # and each day there is no precip, the value decreses based on biome
        # need to remove the duration of precip, its calculated purely each day
        self.args = args
        self.time = time
        self.indv_biomes_config = indv_biomes_config
        self.conn = conn

        master_config = MasterConfig
        self.world_config = master_config.world_config_master
        self.percentile = PercentileCheck()

        self.region_pack = []
        self._get_region_info()  # should be moved into arg buider
        self.precip_event = (
            False  # this should just be here to initialize this variable
        )
        self.precip_chance = BASE_PRECIP_CHANCE
        self.weather_pack = []
        # contains: [day_num, region_id, region biome, precipitation, severity, duration, weight, precip_event]
        self._weather()
        self._sqlite()

    def _get_region_info(self):
        # builds a initial pack with region id, then removes duplicates and appends into region pack
        test_pack = []
        for id in self.indv_biomes_config:
            if id.region_id not in test_pack:
                test_pack.append((id.region_id, id.biome_name))
        [self.region_pack.append(x) for x in test_pack if x not in self.region_pack]

    def _weather(self):
        """weather first pulls a bool from calc_precipitation
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
                duration = 0
                weight = self.get_dry_weight(id)  # returns the dry day weight
            else:
                severity = (
                    self.calc_severity()
                )  # returns 1-5, with extremes having worse weather
                duration = self.calc_duration(
                    severity
                )  # duration baseline is 1, higher severity can be longer
                weight = self.calc_weight(
                    severity
                )  # returns a weight (impact) score (0 - 100)
                self.precip_event = True

            prior_precip_value = self.get_prior_precip_value(id)
            precip_value = int(prior_precip_value) + int(weight)

            self.weather_pack.append(
                (
                    self.time["day_num"],
                    self.time["season_name"],
                    self.region_pack[id][REGION_ID],
                    self.region_pack[id][BIOME_NAME],
                    precipitation,
                    severity,
                    duration,
                    precip_value,
                    self.precip_event,
                )
            )

    def get_prior_precip_value(self, id):
        biome = self.region_pack[id][BIOME_NAME]
        cursor = self.conn.cursor()
        if self.time["day_num"] == 0:
            if biome == "forest":
                start = 0
            elif biome == "plains":
                start = -25
            elif biome == "desert":
                start = -200
            elif biome == "swamp":
                start = 180
            elif biome == "jungle":
                start = 160
            elif biome == "mountain":
                start = -50
            elif biome == "lake" or biome == "river":
                start = 25
            elif biome == "beach":
                start = 50

            return start
        else:
            prior_day_num = self.time["day_num"] - 1
            query = cursor.execute(
                f"""
                SELECT precip_value
                FROM regional_weather
                WHERE day_num = {prior_day_num}
                AND year = {self.time["year"]}
                AND region_id = {self.region_pack[id][REGION_ID]}
                """
            )
            for result in query:
                return result[0]

    def calc_precipitation(self, id):
        """this function takes the base precipitation chance from
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
            season_name = self.time["season_name"]
            if season_name == "summer":
                self.precip_chance = SUMMER_BASE
            elif season_name == "winter":
                self.precip_chance = WINTER_BASE
            elif season_name == "spring":
                self.precip_chance = SPRING_BASE
            else:
                self.precip_chance = FALL_BASE

        def biome_changes():
            biome = self.region_pack[id][BIOME_NAME]
            # forest, plains, desert, swamp, jungle, mountain, lake, river, beach
            if biome == "desert":
                self.precip_chance = self.precip_chance // DESERT_MOD
            elif biome == "mountain":
                self.precip_chance = self.precip_chance // MOUNTAIN_MOD
            elif biome == "jungle":
                self.precip_chance = self.precip_chance * JUNGLE_MOD
            elif biome == "swamp":
                self.precip_chance = self.precip_chance * SWAMP_MOD

        def temp_changes():
            temp_zone = self.args["location_info"]["temp_zone"]
            if temp_zone == 1:
                self.precip_chance = self.precip_chance // ZONE_1_MOD
            elif temp_zone == 5:
                self.precip_chance = self.precip_chance // ZONE_5_MOD
            elif temp_zone == 3:
                self.precip_chance = self.precip_chance * ZONE_3_MOD

        seasonal_changes()
        biome_changes()
        temp_changes()

        if random.randint(0, 100) <= self.precip_chance:
            return True
        else:
            return False

    def get_dry_weight(self, id):
        biome = self.region_pack[id][BIOME_NAME]
        weight = DRY_WEIGHT_BASE
        # fuck with this
        if biome == "forest":
            weight += -2
        elif biome == "plains":
            weight += -2
        elif biome == "desert":
            weight += -1
        elif biome == "swamp":
            weight += -7
        elif biome == "jungle":
            weight += -7
        elif biome == "mountain":
            weight += -2
        elif biome == "lake":
            weight += -2
        elif biome == "river":
            weight += -2
        elif biome == "beach":
            weight += -2
        return weight

    def calc_severity(self):
        temp_zone = self.args["location_info"]["temp_zone"]
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
        """Currently not implemented and only will ever return a value
        of 1. Potentially in the future having longer periods of rain would
        be interesting but at the moment it is purely feature-creep.
        """
        return 1

    #        if severity == 1:
    #            return 1 + random.randint(0, 2)
    #        return 1 + random.randint(0, 1)

    def calc_weight(self, severity):
        # weight inverse -- 6
        # severity - 1-5 leaning towards 5
        # weight multiple mod -- 10
        # weight = (WEIGHT_INVERSE - severity) * WEIGHT_MULTIPLE_MOD
        weight = 5 + ((WEIGHT_INVERSE - severity) / 2)
        return weight

    def _sqlite(self):
        cursor = self.conn.cursor()
        year = self.time["year"]

        for item in self.weather_pack:
            day_num = item[0]
            season = item[1]
            region_id = item[2]
            biome_name = item[3]
            precipitation = item[4]
            severity = item[5]
            duration = item[6]
            precip_value = item[7]
            precip_event = item[8]

            astral_event = None
            natural_event = None

            insert_regional_weather = f"""
                    INSERT INTO regional_weather (
                        day_num, year, season, region_id, biome_name, precipitation,
                        severity, duration, precip_value, precip_event
                        )
                    VALUES (
                        {day_num}, {year}, '{season}', {region_id}, '{biome_name}', {precipitation},
                        {severity}, {duration}, {precip_value}, {precip_event}
                        )
                    """

            insert_master_timeline = f"""
                    INSERT INTO master_timeline (
                        day_num, year, season, region_id, biome_name,
                        precip_event, astral_event, natural_event
                        )
                    VALUES (
                        {day_num}, {year}, '{season}', {region_id}, '{biome_name}',
                        {precip_event}, '{astral_event}', '{natural_event}'
                        )
                    """

            cursor.execute(insert_regional_weather)
            cursor.execute(insert_master_timeline)
        self.conn.commit()
