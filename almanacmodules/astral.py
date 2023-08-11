#!/usr/bin/env/python

"""
"""

# BUILT INS
import random

# THIRD PARTY

# PERSONAL
from almanacmodules import cfg  # initial config that I'm moving away from for most info
from almanacmodules import (
    caller,
)  # works in conjunction with cfg to return items from lists
from almanacmodules.get_sheets import (
    MasterConfig,
)  # usable google sheets in pydantic form


class AstralInfo:
    """returns the information related to an astral event occuring.
    this includes:
        - the reference id number of the astral body
        - the name of astral body
        - the type of the astral body
        - the event or movement that the astral body is experiencing
    """

    def __init__(self):
        # these 3 lines collect the configs for all the astral and effects info
        master_config = MasterConfig()
        self.astral_config = master_config.astral_config_master
        self.effects_config = master_config.effects_config_master

        # class variables
        self.astral_id = None  # id number of an astral body
        self.astral_name = None  # name of rand_astral body
        self.astral_type = None  # type of rand_astral body
        self.p_event_pick = None  # event that the rand_astral body is going through

        self.event_details = []

    def get_astral(self):
        get_array = caller.GetArray()
        self.astral_id = random.randint(0, len(list(self.astral_config)) - 1)

        for row in self.astral_config:
            if row.id == self.astral_id:
                self.astral_type = row.type
                self.astral_name = row.name

        self.p_event_pick = get_array.get_events(
            random.randint(0, (len(cfg.planet_events) - 1))
        )

        self.event_details.append(
            (self.astral_id, self.astral_name, self.astral_type, self.p_event_pick)
        )
        return self.event_details
