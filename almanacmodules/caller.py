#!/bin/env python
from almanacmodules import cfg


class GetArray:
    def __init__(self):  # constructor
        self.year = 1325  # year not currently used except as an example

    def get_seasons(self, current_season=None):
        if current_season is None:
            return cfg.seasons
        else:
            return cfg.seasons[current_season]

    def get_months(self, current_month=None):
        if current_month is None:
            return cfg.months
        else:
            return cfg.months[current_month]

    def get_types(self, day_type=None):
        if day_type is None:
            return cfg.types
        else:
            return cfg.types[day_type]

    def get_events(self, p_event_pick=None):
        if p_event_pick is None:
            return cfg.planet_events
        else:
            return cfg.planet_events[p_event_pick]

    def get_effects(self, m_effect_pick=None):
        if m_effect_pick is None:
            return cfg.monster_effects
        else:
            return cfg.monster_effects[m_effect_pick]
