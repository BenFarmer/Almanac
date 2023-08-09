#!/bin/env python

from almanacmodules.config import world, natural, astral, monster, biome

#               WORLD TEST CONFIGS
test_world_0 = world(
    id="0",
    name="test_world_0",
    type="country",
    forest="100",
    plains="0",
    desert="0",
    swamp="0",
    jungle="0",
    mountain="0",
    lake="0",
    river="0",
    beach="0",
    ocean="0",
    underdark="0",
    urban="0",
    temp_zone="3",
    capital="testopia",
    owner="almanac",
)
test_world_1 = world(
    id="1",
    name="test_world_1",
    type="country",
    forest="100",
    plains="0",
    desert="0",
    swamp="0",
    jungle="0",
    mountain="0",
    lake="0",
    river="0",
    beach="0",
    ocean="0",
    underdark="0",
    urban="0",
    temp_zone="3",
    capital="testopia",
    owner="almanac",
)
test_worlds = test_world_0, test_world_1

#               NATURAL TEST CONFIGS
test_natural_0 = natural(
    id="0",
    name="test_earthquake",
    forest="3",
    plains="3",
    desert="3",
    swamp="3",
    jungle="3",
    mountain="0",
    lake="3",
    river="3",
    beach="3",
    ocean="0",
    underdark="4",
    urban="3",
    season="any",
    temp_zone=["1", "2", "3", "4", "5"],
)
test_natural_1 = natural(
    id="1",
    name="test_thunderstorm",
    forest="4",
    plains="4",
    desert="4",
    swamp="4",
    jungle="4",
    mountain="5",
    lake="4",
    river="4",
    beach="4",
    ocean="5",
    underdark="0",
    urban="4",
    season="summer",
    temp_zone=["3", "4", "5"],
)
test_natural_2 = natural(
    id="2",
    name="test_rare",
    forest="1",
    plains="1",
    desert="1",
    swamp="1",
    jungle="1",
    mountain="1",
    lake="1",
    river="1",
    beach="1",
    ocean="1",
    underdark="1",
    urban="1",
    season="summer",
    temp_zone=["1", "2", "3", "4", "5"],
)
test_natural_3 = natural(
    id="3",
    name="test_very_common",
    forest="5",
    plains="5",
    desert="5",
    swamp="5",
    jungle="5",
    mountain="5",
    lake="5",
    river="5",
    beach="5",
    ocean="5",
    underdark="5",
    urban="5",
    season="summer",
    temp_zone=["1", "2", "3", "4", "5"],
)
test_naturals = test_natural_0, test_natural_1  # , test_natural_2, test_natural_3

#               ASTRAL TEST CONFIGS
test_astral_0 = astral(id="0", name="test_calypso", type="moon", moon_of="saturn")
test_astral_1 = astral(id="1", name="test_mars", type="planet", moon_of="no")

test_astrals = test_astral_0, test_astral_1

#               MONSTER TEST CONFIGS
test_monster_0 = monster(
    id="0",
    name="test_bat",
    type="normal",
    forest="5",
    plains="4",
    desert="2",
    swamp="4",
    jungle="4",
    mountain="2",
    lake="3",
    river="3",
    beach="2",
    ocean="0",
    underdark="3",
    urban="2",
)
test_monster_1 = monster(
    id="1",
    name="test_cat",
    type="normal",
    forest="3",
    plains="2",
    desert="2",
    swamp="0",
    jungle="2",
    mountain="3",
    lake="1",
    river="1",
    beach="1",
    ocean="0",
    underdark="0",
    urban="4",
)
test_monsters = test_monster_0, test_monster_1

#               BIOME TEST CONFIGS
test_biome_0 = biome(id="0", name="test_forest")
test_biome_1 = biome(id="1", name="test_plains")
test_biomes = test_biome_0, test_biome_1
