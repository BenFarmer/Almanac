#!/bin/env python

from almanacmodules.get_sheets import MasterConfig
from almanacmodules.rarity_calc import PercentileCheck
import random


class NaturalInfo:
    """on each day where a natural event is randomly set to happen, up to 5 regions are selected to see what events
    may happen in each respective location. This module assumes that these events do happen, and send the results
    back to be registered and verified by the master timer who may allow one or several depending on several
    conditions."""

    def __init__(self, country_id):
        master_config = None
        self.world_config = None
        self.natural_config = None

        self.country_id = country_id
        self.regions_affected = []  # [[region_info], [natural_event]]
        self.natural_ids = []

        self.percentile_check = PercentileCheck()

    def load_config(self):
        master_config = MasterConfig()
        self.world_config = master_config.world_config_master
        self.natural_config = master_config.natural_config_master
        self._get_ids()

    def _get_ids(self):
        assert self.world_config
        temp_goal = self.world_config[self.country_id].temp_zone
        for row in self.natural_config:
            if int(temp_goal) in list(row.temp_zone):
                self.natural_ids.append(row.id)

    def decide_natural(self, indv_biomes_config):
        region_count = 6 - (self.percentile_check.norm_rarity())
        for num in range(region_count):
            region = indv_biomes_config[
                random.randint(0, len(list(indv_biomes_config)) - 1)
            ]
            biome = region.biome_name
            names = self._get_names(biome)
            severity = self.percentile_check.norm_rarity()
            if len(names) == 0:
                return self.regions_affected
            else:
                self.regions_affected.append(
                    (region, names[random.randint(0, (len(names) - 1))], severity)
                )
                return self.regions_affected

    def _get_names(self, biome):
        rarity = self.percentile_check.norm_rarity()

        natural_names = []
        for row in self.natural_config:
            if row.id in self.natural_ids:
                if biome == "forest":
                    if row.forest == rarity:
                        natural_names.append(row.name)
                elif biome == "plains":
                    if row.plains == rarity:
                        natural_names.append(row.name)
                elif biome == "desert":
                    if row.desert == rarity:
                        natural_names.append(row.name)
                elif biome == "swamp":
                    if row.swamp == rarity:
                        natural_names.append(row.name)
                elif biome == "jungle":
                    if row.jungle == rarity:
                        natural_names.append(row.name)
                elif biome == "mountain":
                    if row.mountain == rarity:
                        natural_names.append(row.name)
                elif biome == "lake":
                    if row.lake == rarity:
                        natural_names.append(row.name)
                elif biome == "river":
                    if row.river == rarity:
                        natural_names.append(row.name)
                elif biome == "beach":
                    if row.beach == rarity:
                        natural_names.append(row.name)
        return natural_names


#                if biome == "ocean":
#                    if row.ocean == rarity:
#                        natural_names.append(row.name)
#                if biome == "underdark":
#                    if row.underdark == rarity:
#                        natural_names.append(row.name)
#                if biome == "urban":
#                    if row.urban == rarity:
#                        natural_names.append(row.name)
