#!/usr/bin/env bash

if [ ! -x "$(command -v hddtemp)" ]; then
	sudo apt install hddtemp
fi

# TODO sudo is needed for hddtemp, right? so sudo crontab?

this_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# (every minute, which is the most frequent cron will do something)
new_cron_line="* * * * * ${this_script_dir}/check_hdd_temps.py"
# From TheBonsai's answer https://stackoverflow.com/questions/878600
sudo crontab -l | { cat; echo "$new_cron_line"; } | sudo crontab -

