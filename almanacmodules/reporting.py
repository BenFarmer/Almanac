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

        self.event_counts()
        self.location_info()

        self.location_table, self.arg_table = self.build_tables()
        self.pop_arg_table()
        self.pop_loc_table()
        self.output_tables()

    def event_counts(self):
        def potential_astral():
            """There should not be many astral or natural events that will
            attempt to happen so our tables will be quite small. because
            of this the reporting and analysis of these tables will be handled
            in python and not in SQL
            """
            query = self.cursor.execute("""SELECT * FROM astral_events""")
            events = []
            for result in query:
                events.append(result)

            # this is a pretty sloppy way to do this
            counts = {
                "event": 0,
                "plnt": 0,
                "moon": 0,
                "spring": 0,
                "summer": 0,
                "winter": 0,
                "fall": 0,
            }

            for event in events:
                counts["event"] += 1
                if event[1] == "spring":
                    counts["spring"] += 1
                elif event[1] == "summer":
                    counts["summer"] += 1
                elif event[1] == "winter":
                    counts["winter"] += 1
                elif event[1] == "fall":
                    counts["fall"] += 1
                elif event[3] == "moon":
                    counts["moon"] += 1
                elif event[3] == "planet":
                    counts["plnt"] += 1
                print(event[3])
            print(counts)

        def potential_natural():
            query = self.cursor.execute("""SELECT * FROM natural_events""")
            events = []
            for result in query:
                events.append(result)

        potential_astral()
        potential_natural()

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
        arg_table.add_column("sub dictionary key", style="cyan", no_wrap=True)
        arg_table.add_column("key", style="magenta", no_wrap=True)
        arg_table.add_column("value", style="magenta", no_wrap=True)

        return location_table, arg_table

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

    def output_tables(self):
        console = Console()
        console.print(self.location_table)
        console.print(self.arg_table)
