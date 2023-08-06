# Pomodoro Calculator

A command line tool to calculate the number of Pomodoros available between two
points in time.

![Pomodoro Calculator screenshot](https://codeberg.org/Dokana/Pomodoro-Calculator/raw/branch/trunk/screenshot.png)


## Installation

You can install the **Pomodoro Calculator** using pip:

```console
    $ pip install pomodoro-calculator
```


## Usage

Use the `get-pomodori` command from the shell to run Pomodoro Calculator:

```console
    $ get-pomodori --help
    Calculate the number of Pomodori available within a time period.

    Usage:
      get-pomodori [--pomodoro=<time>] [--from=<time>] [--break=<minutes>] [--long-break=<minutes>]
                   [--group=<pomodori>] [--interval] [--json] [--nocolour] [--amount] [--extensive-report] <end-time>
      get-pomodori (-h | --help | --version)

    Options:
      --version                   show program's version number and exit.
      -h, --help                  show this help message and exit.
      -i, --interval              specify that the end time is a time interval, not a time of day.
      -f, --from=<time>           calculate available Pomodori from this time [default: now].
      -b, --break=<minutes>       the amount of minutes between each Pomodori [default: 5].
      -l, --long-break=<minutes>  the amount of minutes between every four Pomodori [default: 15].
      -p, --pomodoro=<minutes>    the amount of minutes for every pomodoro session [default: 25].
      -g, --group=<pomodori>      the amount of pomodori before a long break [default: 4].
      -j, --json                  output the pomodori schedule in JSON format.
      -n, --nocolour              do not colourise the output.
      -a, --amount                specify that the end time is the number of pomodoros you desire to do, not the time of a day.
      -x, --extensive-report      also write total break time and total session time.
```


## Licence

Copyright © 2023 Matthew Stevens, released under the [ISC Licence](https://codeberg.org/Dokana/Pomodoro-Calculator/src/branch/trunk/LICENCE).
