#!/bin/env python

""" this controls the pydantic BaseModels for various events to
    be referenced by event_coordinator to determine if events are
    able to occur
"""


# THIRD PARTY
from pydantic import BaseModel

class NaturalRule(BaseModel):
    name: str               # name of natural event rule

    period: int             # how many days prior need to be looked at for rule
                                # for rule[FLOOD], 7 days need to be looked at
                                # for rule[DROUGHT], 30 days need to be looked at

    precip_score: int       # of the days looked at, how value needs to be met
                                # for rule[FLOOD], score needs to exceed 190
                                # for rule[DROUGHT], score needs to be under 20

    #precip_mod: str        # + or - to signify above or below the precip_score?

    base_duration: int      # how many days does this last
                                # for rule[FLOOD], base duration is 2 days
                                # for rule[DROUGHT], base duration is 45
                                    # drought lowers all precip severity during its duration?

flood_data = {
        'name': 'flood',
        'period': 7,
        'precip_score': 190,
        'base_duration': 2,
        }


drought_data = {
        'name': 'drought',
        'period': 30,
        'precip_score': 30,
        'base_duration': 45,
        }

_data = {
        'name': '',
        'period': ,
        'precip_score': ,
        'base_duration': ,
        }

rule_flood = NaturalRule(**flood_data)


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
