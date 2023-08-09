#!/bin/env python

from almanacmodules.calender import DayInfo
import pytest


class TestCalender:
    run_times = 100
    country_select = "test_country_select"
    day_info = DayInfo(country_select)

    def test_event_picker(self):
        print("test event picker in calender")
        for test_num in range(run_times):
            test_output = day_info.event_picker(season_num=1)
            print(
                "\ntest number:",
                test_num,
            )


# need to figure out how to return a variable (day_type) from this function without it
# calling the decider module
