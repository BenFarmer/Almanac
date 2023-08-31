#!/bin/env python

# BUILT-INS

# THIRD PARTY
from rich.console import Console
from rich.table import Table

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

        self.event_counts()
        self.location_info()

        self.location_table, self.arg_table, self.report_table = self.build_tables()
        self.pop_arg_table()
        self.pop_loc_table()
        self.pop_report_table()
        self.output_tables()

    def event_counts(self):
        def count_potential_astral_event():
            query = self.cursor.execute("""SELECT COUNT (*) FROM astral_events""")
            for result in query:
                self.reports["astral_events"]["astral count"] = result[0]

        def count_potential_natural_event():
            query = self.cursor.execute("""SELECT COUNT (*) FROM natural_events""")
            for result in query:
                self.reports["natural_events"]["natural count"] = result[0]

        def count_master_precip_event():
            query = self.cursor.execute(
                """SELECT COUNT (*) FROM master_timeline WHERE precip_event=1"""
            )
            for result in query:
                self.reports["master_timeline"]["precipitation count"] = result[0]

        # what_type_where_what
        count_potential_astral_event()
        count_potential_natural_event()
        count_master_precip_event()

    def location_info(self):
        print("location_info")

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

        return location_table, arg_table, report_table

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
        print(self.reports)
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

    def output_tables(self):
        console = Console()
        console.print(self.location_table)
        console.print(self.arg_table)
        console.print(self.report_table)
