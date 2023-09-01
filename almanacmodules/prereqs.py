#!/bin/env python

""" this controls the pydantic BaseModels for various events to
    be referenced by event_coordinator to determine if events are
    able to occur
"""


# THIRD PARTY
from pydantic import BaseModel


class high_precip(BaseModel):
    # flood, snowstorm, mudslide
    precip_period: int  # 7 (days)
    precip_score: int  # <= 190


class low_precip(BaseModel):
    # drought, wildfire
    precip_period: int  # 30 (days)
    precip_score: int  # >= 20


class NaturalPreReqs:
    def __init__(self):
        # days prior, score requirement, over/under
        self.flood = [7, 190, "over"]
        self.drought = [30, 20, "under"]

    # blizzard, drought, earthquake, flood, hail_storm, hurricane, landslide,
    # sandstorm, sinkhole, thunderstorm, tornado, tsunami, wildfire

    # EASY - country temp zone, correct season, correct biome
    # DIFFICULT - previous weather,

    def blizzard_reqs(self):
        print("prereqs")
