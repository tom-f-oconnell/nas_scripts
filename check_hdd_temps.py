#!/usr/bin/env python3

"""
Checks HDD temps and sends an email alert if they are too high.
"""

from subprocess import check_output, CalledProcessError
import tempfile
import socket
from os.path import join, exists, getmtime
from pathlib import Path
import time
from datetime import datetime, timedelta

# TODO need to do other stuff on install to have access to this
# (since this script may be being called from whatever cwd of cron is)
from gmail_notifier import send_email


# TODO run this once on setup so installer can see which drives are being
# reported on / fix problems
def main():
    try:
        # assumes python script is called as superuser (no sudo prefix)
        # need shell=True if we are going to relay on shell ? feature
        # to enumerate the drives
        hddtemp_out = check_output('hddtemp /dev/sd?', shell=True)
    except CalledProcessError as e:
        #print(e.out)
        raise

    report_temp_celsius = 45
    shutdown_temp_celsius = 50
    min_report_period_s = 60 * 60 * 3
    assert (shutdown_temp_celsius is None or
        shutdown_temp_celsius >= report_temp_celsius
    )

    tmp_dir = tempfile.gettempdir()
    last_report_file = join(tmp_dir, 'check_hdd_temps_last_report')

    hddtemp_out = hddtemp_out.decode()
    lines = hddtemp_out.splitlines()
    for line in lines:
        line = line.strip()
        if not line.endswith('°C'):
            continue
        parts = line.split()
        try:
            temp_c = float(parts[-1][:-2])
            import ipdb; ipdb.set_trace()
        except ValueError as e:
            print(e)
            continue
        import ipdb; ipdb.set_trace()

        if temp_c >= report_temp_celsius:
            if (not exists(last_report_file) or
                getmtime(last_report_file) + min_report_period_s < time.time()):

                soonest_next_email = \
                    datetime.now() + timedelta(seconds=min_report_period_s)

                message = (f'host: {socket.gethostname()}\n{datetime.now()}'
                    f'\n\n{hddtemp_out}\n\n'
                    'No report will be sent until {soonest_next_email}!'
                )

                send_email(subject='WARNING! High NAS drive temperatures!',
                    message=message
                )
                Path(last_report_file).touch()

            # TODO maybe try unmounting before shutting down or something?


if __name__ == '__main__':
    main()

