#!/bin/env python

from almanacmodules.astral import AstralInfo  # astral class in astral.py
from almanacmodules.tests.test_feed_data import astral

import pytest


class TestAstral:
    def test_astral_output(self):
        """test the output a set amount of times"""
        run_times = 100

        monster_name = "test monster"
        biome_id = 0

        astral_info = AstralInfo(biome_id, monster_name)
        #       this would be used if i wanted to sub out the master astral config
        #        astral_info.astral_config =
        print(f"running {run_times} tests")
        for test_num in range(run_times):
            test_output = astral_info.get_astral()
            print("\ntest number:", test_num, test_output)

    def test_get_astral(self):
        run_times = 100
