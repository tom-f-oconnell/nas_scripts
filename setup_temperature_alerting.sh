#!/usr/bin/env bash

if [ ! -x "$(command -v hddtemp)" ]; then
	sudo apt install hddtemp
    # For CPU temp:
    sudo apt install lm-sensors
    # Will probably need to do these two interactively:
    sudo sensors-detect
    # (from linked SO post, though from 2010) "You may also need to run"
    # sudo service kmod start
fi

this_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
py_script="${this_script_dir}/check_temperatures.py"


# (every minute, which is the most frequent cron will do something)
new_cron_line="* * * * * $py_script"
# From TheBonsai's answer https://stackoverflow.com/questions/878600
sudo crontab -l | { cat; echo "$new_cron_line"; } | sudo crontab -

# TODO run hddtemp / command to get CPU temp once here (or just run python
# script that generates them, w/ arg to print command outputs), so
# installer can tell to what extent things are working + fix if not

