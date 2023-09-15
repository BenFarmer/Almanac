#!/bin/env python

# BUILT-INS

# THIRD PARTY
from rich.console import Console
from rich.table import Table
from rich import print

import plotly.express as px
import plotly.graph_objects as go

# PERSONAL


class Reports:
    def __init__(self, master_config, args, time, conn):
        self.master_config = master_config
        self.world_config = master_config.world_config_master
        self.args = args
        self.time = time
        self.conn = conn
        self.cursor = conn.cursor()
        self.reports = {
            "astral_events": {},
            "natural_events": {},
            "master_timeline": {},
        }
        self.weather_reports = {
            "avg precip value": {},
            "avg season precip value": {},
        }

        self.event_counts()

        (
            self.location_table,
            self.arg_table,
            self.report_table,
            self.weather_table,
        ) = self.build_tables()
        self.pop_arg_table()
        self.pop_loc_table()
        self.pop_report_table()
        self.pop_weather_table()
        self.output_tables()
        self.output_graphs()

    def event_counts(self):
        def count_potential_event(table):
            query = self.cursor.execute(f"""SELECT COUNT (*) FROM {table}""")
            for result in query:
                self.reports[f"{table}"]["total number of events"] = result[0]

        def avg_potential_event(table):
            query = self.cursor.execute(
                f"""
                    SELECT avg(count)
                    FROM (
                        SELECT COUNT(*) as count
                        FROM {table} T
                        GROUP BY T.year
                        )"""
            )
            for result in query:
                self.reports[f"{table}"]["average amount of events/year"] = result[0]

        def max_potential_event(table):
            query = self.cursor.execute(
                f"""
                    SELECT max(count)
                    FROM (
                        SELECT COUNT(*) as count
                        FROM {table} T
                        GROUP BY T.year
                        )"""
            )
            for result in query:
                self.reports[f"{table}"]["highest amount of events/year"] = result[0]

        def min_potential_event(table):
            query = self.cursor.execute(
                f"""
                    SELECT min(count)
                    FROM (
                        SELECT COUNT(*) as count
                        FROM {table} T
                        GROUP BY T.year
                        )"""
            )
            for result in query:
                self.reports[f"{table}"]["least amount of events/year"] = result[0]

        def most_common_season(table):
            query = self.cursor.execute(
                f"""
                SELECT max(count), season
                FROM (
                    SELECT COUNT(*) as count, season
                    FROM {table} T
                    GROUP BY T.season
                )"""
            )
            for result in query:
                self.reports[f"{table}"]["season with the most total events"] = (
                    result[0],
                    result[1],
                )

        # NATURAL EVENT SPECIFIC
        def most_common_biome():
            query = self.cursor.execute(
                """
                    SELECT max(count), biome_name
                    FROM (
                        SELECT COUNT(*) as count, biome_name
                        FROM natural_events T
                        GROUP BY T.biome_name
                    )"""
            )
            for result in query:
                self.reports["natural_events"]["biome with the most total events"] = (
                    result[0],
                    result[1],
                )

        # MASTER TIMELINE SPECIFIC
        def count_master_precip_event():
            query = self.cursor.execute(
                """SELECT COUNT (*) FROM master_timeline WHERE precip_event=1"""
            )
            for result in query:
                self.reports["master_timeline"][
                    "total number of precip events"
                ] = result[0]

        def count_master_astral_event():
            self.reports["master_timeline"][
                "total number of astral_events"
            ] = "not yet implemented"

        # WEATHER SPECIFIC
        def avg_weather_biome():
            for season in self.time["seasons"]:
                for biome in self.args["location_info"]["biomes"]:
                    query = self.cursor.execute(
                        f"""
                        SELECT ROUND(AVG(precip_value))
                        FROM regional_weather
                        WHERE biome_name = "{biome}"
                        AND season = "{season}"
                        """
                    )
                    for result in query:
                        self.weather_reports["avg precip value"][
                            f"{biome} in {season}"
                        ] = result[0]

        def avg_weather_season():
            for season in self.time["seasons"]:
                query = self.cursor.execute(
                    f"""
                    SELECT ROUND(AVG(precip_value))
                    FROM regional_weather
                    WHERE season = "{season}"
                    """
                )
                for result in query:
                    self.weather_reports["avg season precip value"][
                        f"{season}"
                    ] = result[0]

        # what_type_where_what
        try:
            for event in self.args["event"]["event_names"]:
                table = f"{event}_events"
                count_potential_event(table)
                avg_potential_event(table)
                min_potential_event(table)
                max_potential_event(table)
                most_common_season(table)
            most_common_biome()
            count_master_precip_event()

            avg_weather_biome()
            avg_weather_season()
        except OSError as e:
            print(e)

    def build_tables(self):
        # EXPANDED LOCATION TABLE
        location_table = Table(
            title=f"Statistics of {self.args['location_info']['location_name']}",
            caption="statistics taken from google sheet",
        )
        location_table.add_column("field", justify="right", style="cyan", no_wrap=True)
        location_table.add_column("value", style="magenta", no_wrap=True)

        # ARGUMENT TABLE
        arg_table = Table(
            title="ARGUMENTS",
            caption="argument dictionary used in current run of Almanac",
        )
        arg_table.add_column("sub dictionary key", style="red", no_wrap=True)
        arg_table.add_column("key", style="magenta", no_wrap=True)
        arg_table.add_column("value", style="cyan", no_wrap=True)

        # REPORT TABLE
        report_table = Table(
            title="REPORTS",
            caption="various reports run on Almanac results",
        )
        report_table.add_column("topic", style="red", no_wrap=True)
        report_table.add_column("report", style="cyan", no_wrap=True)
        report_table.add_column("result", style="magenta", no_wrap=True)

        # WEATHER TABLE
        weather_table = Table(
            title="WEATHER REPORTS",
            caption="weather reporting throughout Almanac",
        )
        weather_table.add_column("focus", style="red", no_wrap=True)
        weather_table.add_column("report", style="cyan", no_wrap=True)
        weather_table.add_column("result", style="magenta", no_wrap=True)

        return location_table, arg_table, report_table, weather_table

    def pop_loc_table(self):
        for country in self.world_config:
            if country.id == self.args["location_info"]["location_id"]:
                for field in country:
                    self.location_table.add_row(f"{field[0]}", f"{field[1]}")

    def pop_arg_table(self):
        sub_dict_keys = list(self.args)
        for sub_dict in sub_dict_keys:
            keys = list(self.args[sub_dict])
            for num, i in enumerate(keys):
                value = list(self.args[sub_dict].values())
                if value[num] == value[0]:
                    self.arg_table.add_row(f"{sub_dict}", f"{i}", f"{value[num]}")
                elif value[num] == value[-1]:
                    self.arg_table.add_row(
                        "", f"{i}", f"{value[num]}", end_section=True
                    )
                else:
                    self.arg_table.add_row("", f"{i}", f"{value[num]}")

    def pop_report_table(self):
        sub_dict_keys = list(self.reports)
        for sub_dict in sub_dict_keys:
            keys = list(self.reports[sub_dict])
            for num, i in enumerate(keys):
                value = list(self.reports[sub_dict].values())
                if value[num] == value[0]:
                    self.report_table.add_row(f"{sub_dict}", f"{i}", f"{value[num]}")
                elif value[num] == value[-1]:
                    self.report_table.add_row(
                        "", f"{i}", f"{value[num]}", end_section=True
                    )
                else:
                    self.report_table.add_row("", f"{i}", f"{value[num]}")

    def pop_weather_table(self):
        sub_dict_keys = list(self.weather_reports)
        for sub_dict in sub_dict_keys:
            keys = list(self.weather_reports[sub_dict])
            for num, i in enumerate(keys):
                value = list(self.weather_reports[sub_dict].values())
                if value[num] == value[0]:
                    self.weather_table.add_row(f"{sub_dict}", f"{i}", f"{value[num]}")
                elif value[num] == value[-1]:
                    self.weather_table.add_row(
                        "", f"{i}", f"{value[num]}", end_section=True
                    )
                else:
                    self.weather_table.add_row("", f"{i}", f"{value[num]}")

    def output_tables(self):
        console = Console()
        console.print(self.location_table)
        console.print(self.arg_table)
        console.print(self.report_table)
        console.print(self.weather_table)

    def output_graphs(self):
        """This SQL code returns each biome and its avg precip value for each day
        across every single day
        EX. result:
        ('lake',    205,    70.5)
        [0]         [1]     [2]
        biome       day     avg_val
        """
        for day in range(self.args["year_info"]["max_day"]):
            query = self.cursor.execute(
                f"""
                SELECT biome_name,
                        {day} AS n_day,
                        ROUND(AVG(precip_value), 2)
                FROM regional_weather
                WHERE day_num = {day}
                GROUP BY biome_name
                """
            )
            for result in query:
                print(result)
                return
        fig = px.bar(x=["a", "b", "c"], y=[1, 2, 3])
        fig_widget = go.FigureWidget(fig)
        fig.show()
        fig_widget
