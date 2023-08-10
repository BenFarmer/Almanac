#!/bin/env python

""" this controls the pydantic BaseModels for various events to
    be referenced by event_coordinator to determine if events are
    able to occur
"""


# THIRD PARTY
from pydantic import BaseModel


class flood(BaseModel):
    precip_period: int  # 7 (days)
    precip_score: int  # <= 190


class drought(BaseModel):
    precip_period: int  # 30 (days)
    precip_score: int  # >= 20


class NaturalPreReqs:
    def __init__(self):
        # days prior, score requirement, over/under
        self.flood = [7, 190, "over"]
        self.drought = [30, 20, "under"]

    #        self.
    #        self.
    #        self.
    #        self.
    #        self.
    #        self.
    #        self.
    #        self.
    # blizzard, drought, earthquake, flood, hail_storm, hurricane, landslide,
    # sandstorm, sinkhole, thunderstorm, tornado, tsunami, wildfire

    # EASY - country temp zone, correct season, correct biome
    # DIFFICULT - previous weather,

    # EXAMPLE - flooding can only occur if it has rained at minimum 3 times
    # in the last week

    def blizzard_reqs(self):
        print("prereqs")
