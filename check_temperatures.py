#!/usr/bin/env python3

"""
Checks HDD temps and sends an email alert if they are too high.

Can also be configured to shutdown NAS if temperatures reach another threshold.
"""

from subprocess import check_output, Popen
import tempfile
import socket
from os.path import join, exists, getmtime
from pathlib import Path
import time
from datetime import datetime, timedelta

# TODO need to do other stuff on install to have access to this
# (since this script may be being called from whatever cwd of cron is)
from gmail_notifier import send_email


# TODO add argument to only print out all the drive temps not send email /
# shutdown (despite whether current temps are > threshold)
# TODO option to print both thresholds, as well as time(s) required to exceed
# threshold(s), if applicable


# TODO run this once on setup so installer can see which drives are being
# reported on / fix problems
def main():
    # assumes python script is called as superuser (no sudo prefix)
    # need shell=True if we are going to relay on shell ? feature
    # to enumerate the drives
    hddtemp_out = check_output('sudo hddtemp /dev/sd?', shell=True).decode()
    #sensors_out = check_output('sensors').decode()

    min_report_period_s = 60 * 60 * 3

    hdd_report_temp_celsius = 45
    #hdd_shutdown_temp_celsius = 50
    # TODO is 50 really much better than recommended range reported w/ 
    # `sudo smartctl -x /dev/sda`, in a line like this one:
    # `Min/Max recommended Temperature:      0/60 Celsius`
    hdd_shutdown_temp_celsius = 60
    assert (hdd_shutdown_temp_celsius is None or
        hdd_shutdown_temp_celsius >= hdd_report_temp_celsius
    )

    # TODO could get these bounds from `sensors` output (high / crit, for most)
    # unclear exactly which values to use. (could) use max of possible vals?
    # https://askubuntu.com/questions/843231
    #cpu_report_temp_celsius = 
    #cpu_shutdown_temp_celsius = 

    tmp_dir = tempfile.gettempdir()
    last_report_file = join(tmp_dir, 'check_temps_last_report')

    # TODO i heard somewhere online that SMART data also includes a counter of #
    # spinups. report if the rate of these is particularly high, as this also
    # means the drives may fail early

    # TODO also check + report/shutdown w/ thresholds on CPU temp

    lines = hddtemp_out.splitlines()
    for line in lines:
        line = line.strip()
        if not line.endswith('°C'):
            continue
        parts = line.split()
        try:
            temp_c = float(parts[-1][:-2])
        except ValueError as e:
            print(e)
            continue

        if temp_c >= hdd_report_temp_celsius:
            if not exists(last_report_file):
                send_warning = True
            elif getmtime(last_report_file) + min_report_period_s < time.time():
                send_warning = True
            else:
                send_warning = False

            if send_warning:
                # TODO factor out for sharing w/ cpu temp (or other means of)
                # report triggering
                soonest_next_email = \
                    datetime.now() + timedelta(seconds=min_report_period_s)

                message = (f'Host: {socket.gethostname()}\n{datetime.now()}'
                    f'\n\n{hddtemp_out}\n'
                    f'Next warning will not be sent until {soonest_next_email}!'
                )

                print('sending email')
                send_email(subject='WARNING! High NAS drive temperatures!',
                    message=message
                )
                Path(last_report_file).touch()

                # Temperatures of other drives will already be sent in the
                # email triggered by the first drive in this loop.
                break

            if temp_c >= hdd_shutdown_temp_celsius:
                # TODO maybe try unmounting before shutting down or something?
                Popen('sudo shutdown now'.split())


if __name__ == '__main__':
    main()

