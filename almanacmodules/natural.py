#!/bin/env python

# BUILT IN
import random

# PERSONAL
from almanacmodules.get_sheets import MasterConfig
from almanacmodules.rarity_calc import PercentileCheck


class NaturalInfo:
    """on each day where a natural event is randomly set to happen,
    up to 5 regions are selected to experience this event in their respective location.
    natural.py does not validate if these events 'can' happen as that process
    is done through the master timer. Instead these are sent back to the
    event_coordinator and pushed into the natural_events sqlite table.
    """
    def __init__(self, country_id):
        master_config = None
        self.world_config = None
        self.natural_config = None

        self.country_id = country_id
        self.regions_affected = []  # [[region_info], [natural_event]]
        self.natural_ids = []

        self.percentile_check = PercentileCheck()

    def load_config(self):
        """ natural.py is called through this load_config function.
            This allows me to plug in my own testing configs
            in place of the Almanac master_config to get more accurate
            results from testing. This is also why the configs in
            in the __init__ are None.
        """
        master_config = MasterConfig()
        self.world_config = master_config.world_config_master
        self.natural_config = master_config.natural_config_master
        self._get_ids()

    def _get_ids(self):
        """ _get_ids returns the natural disasters that could potentially
            occur in the selected country based on that countries and
            stores them in the self.natural_ids variable.
            temp_zone value.
            Example:    a country with a temp_zone value of 5 (very hot)
                        will not experience a blizzard.
        """
        assert self.world_config
        temp_goal = self.world_config[self.country_id].temp_zone
        for row in self.natural_config:
            if int(temp_goal) in list(row.temp_zone):
                self.natural_ids.append(row.id)

    def decide_natural(self, indv_biomes_config):
        """ decide_natural determines what individual biomes within the
            country experience a natural event.
            Note that up to 5 regions may experience a natural event at
            one time, but it is very unlikely and can be adjusted from the
            rarity_calc module.
            This function then determines a severity for each of the natural
            events and returns a list called self.regions_affected
            which contains:
                [region_id, name of natural event, severity]
        """
        region_count = 6 - (self.percentile_check.norm_rarity())
        for num in range(region_count):
            region = indv_biomes_config[
                random.randint(0, len(list(indv_biomes_config)) - 1)
            ]
            biome = region.biome_name
            names = self._get_names(biome)
            severity = self.percentile_check.norm_rarity()
            if len(names) == 0: # if no regions experience an event
                return self.regions_affected
            else:
                self.regions_affected.append(
                    (region, names[random.randint(0, (len(names) - 1))], severity)
                )
                return self.regions_affected

    def _get_names(self, biome):
        """ get_names is called from decide_natural and returns
            a single name of a natural_event that can occur within
            the biome of the region where it is happening.
            Note that depending on the rarity of the event and the
            biome where it is taking place, no event may occur.
            This is done to make natural events appropriately rare.
        """
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
