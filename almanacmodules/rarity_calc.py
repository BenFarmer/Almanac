#!/bin/env python

""" rarity_calc serves as a singular place to change the probability
    of most events through the Almanac run.
    Most events use the norm_rarity, which returns a 1 - 5 value
    skewed towards the higher numbers
"""


# BUILT INS
import random


class PercentileCheck:
    def __init__(self):
        self.test_100 = random.randint(1, 100)

    def norm_rarity(self):
        # returns a rarity of 1 through 5, skewed towards 5
        self.test_100 = random.randint(1, 100)
        if self.test_100 <= 5:  # 1-5
            grade = 1
        elif self.test_100 <= 15 and self.test_100 > 5:  # 6-15
            grade = 2
        elif self.test_100 <= 35 and self.test_100 > 15:  # 16-35
            grade = 3
        elif self.test_100 <= 65 and self.test_100 > 35:  # 36-65
            grade = 4
        elif self.test_100 <= 100 and self.test_100 > 65:  # 66-100
            grade = 5
        return grade

    def even_rarity(self):
        # returns a rarity of 1 through 5 that is evenly split
        grade = random.randint(1, 5)
        return grade

    def bool_rarity(self):
        grade = random.randint(0, 1)
        if grade == 0:
            return True
        else:
            return False
