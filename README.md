# Almanac: Comprehensive world building utility to bring homebrew world a little bit more life.

# Overview <a name="overview_content"></a>
Welcome to Almanac, a commprehensive world building utility to bring some life to your fantasy world.
My goal with Almanac is to provide a fully customizable simulator to a world of your creation that changes, grows, and reacts, in a *somewhat* realistic manner.
For each single run of Almanac, an entire years worth of information is generated including:
- regional weather (based on temperature zones, time of year, and local biomes)
- astral movements (the passing of religiously important comets, eclipses of the sun, etc.)
- natural disasters (flooding caused by excessive moisture, earthquakes, hurricanes)
Along with the effects that these events may have on local flora and fauna!
~~~
Day 202, Winter of Songs in the year 1325:
Neptune is in retrograde and local moth populations have expanded greatly as a result.
A local village has been destroyed!
~~~
or
~~~
Day 30, Spring of Moonsorrow in the year 1375:
Due to increased rainfall, the plains of Ezoya are currently flooding!
Refugees of flooding have arrived in nearby cities.
Several local villages have been destroyed!
Religious influence has increased!
~~~


# TABLE OF CONTENTS
1. ### [Overview](#overview_content)
2. ### [Usage](#usage_content)
  - [Installation](#installation_content)
  -   - Google Sheets
      - SQLite
  - [Running Almanac](#running_content)
  -   - [Arguments and Configs](#arguments_content)
      - Almanac capabilities and expectations

3. ### [Credits](#credits_content)
4. ### [License](#license_content)
---


# Usage <a name="usage_content"></a>
## Installation <a name="installation_content"></a>
### Google Sheet Setup
- setting up credentials to connect to google api
- copying a version of the extended_cfg sheet
- 
### SQLite Setup
- creating the local SQLite DB
- 
## Running Almanac <a name="running_content"></a>
### Arguments and Configs <a name="arguments_content"></a>
**Required Arguments**
```
-i --input_country    -i <country name>   name of recognized location to be used in Almanac
```

**Optional Arguments**
```
-l --logging_level    -l <level>          sets the logging level of Almanac (default: CRITICAL)

-d --delete_logs      -d <y/n>            indicates if you would like to delete prior logs (default: N)

-r --report           -r <y/n>            indicates if you would like reports to be output into the CLI (default: N)
```

**Configs** (stored within the configs.yaml file)
```
season_num_start      def: 0        index of seasons that dictates what season the year begins in

year_num              def: 1325     starting year of Almanac, not currently used outside of flavor reasons

seasons               def: ['spring', 'summer', 'winter', 'fall']      names of seasons used by Almanac
              (note that changing the names of the seasons here does not change their attributes)

months_in_year        def: 12       months within each year

max_day               def: 366      days within each year

season_length         def: 3        months within each season

month_length          def: 30       days within each month

start_day             def: 1        day number Almanac starts on

rand_event_chance     def: 10       chance that an event will *attempt* to occur on each day

event_names           def: ['astral', 'natural']      names of the types of events that could happen randomly

base_precip_chance    def: 0        baseline precipitation chance used to calculate each biomes chance of rain
```
### Expectations and Limitations of Almanac


# CREDITS <a name="credits_content"></a>
1. Benjamin Farmer - San Juan Data LLC. (2023)

# License <a name="license_content"></a>
*Copyright (c) [2023] [Benjamin Farmer]*

*Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.*

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
