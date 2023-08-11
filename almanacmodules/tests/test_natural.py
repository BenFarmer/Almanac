#!/bin/env python

from almanacmodules.natural import NaturalInfo
from almanacmodules.tests.feed_data import test_worlds, test_naturals


class TestNatural:
    def test_correct_outputs(self):
        run_times = 1000
        biome_name = "forest"
        country_id = 0

        natural_info = NaturalInfo(biome_name, country_id)
        natural_info.natural_config = test_naturals
        natural_info.world_config = test_worlds

        no_names = 0
        single_name = 0
        multiple_names = 0

        for test_num in range(run_times):
            natural_info.get_ids()
            num = len(natural_info.natural_names)
            if num is None:
                no_names += 1
            if num == 1:
                single_name += 1
            if num > 1:
                multiple_names += 1
        print(f"no names collected:{no_names}")
        print(f"single name collected:{single_name}")
        print(f"multiple names collected:{multiple_names}")

    def test_event_chances(self):
        run_times = 100
        biome_name = "forest"
        country_id = 0

        natural_info = NaturalInfo(biome_name, country_id)
        natural_info.natural_config = test_naturals
        natural_info.world_config = test_worlds

        thunderstorms = 0
        earthquakes = 0

        for test_num in range(run_times):
            natural_info.get_ids()
            print(natural_info.last_name)
            if natural_info.last_name == "test_earthquake":
                earthquakes += 1
            elif natural_info.last_name == "test_thunderstorm":
                thunderstorms += 1
        earthquake_chance = (earthquakes / run_times) * 100
        thunderstorm_chance = (thunderstorms / run_times) * 100
        print("thunderstorms:", thunderstorms, "earthquales:", earthquakes)
        print(earthquake_chance, thunderstorm_chance)
        assert 26 < thunderstorm_chance < 34
        assert 16 < earthquake_chance < 24
