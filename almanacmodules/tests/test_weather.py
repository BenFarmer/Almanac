#!/bin/env python

from almanacmodules.weather import DailyWeather


class TestWeather:
    def test_output(self):
        run_times = 100

        daily_weather = DailyWeather
        for test_num in range(run_times):
            test_output = daily_weather.daily_weather()
            print(test_output)
