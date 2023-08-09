#!/bin/env/ python

import argparse


class AlmanacParse:
    def __init__(
        self,
    ):  # needs to be passed arguments from main
        parser = argparse.ArgumentParser()
        parser.add_argument(
            dest="imput_country", help="name of the country that Almanac will use"
        )
        parser.add_argument(
            dest="log_reset", help="a value of " r" will reset previous logs (if any)"
        )

        args = parser.parse_args()
        self.input_country = args.input_country
        self.log_reset = args.log_reset
