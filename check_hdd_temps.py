#!/usr/bin/env python3

"""
Checks HDD temps and sends an email alert if they are too high.
"""

from subprocess import check_output, CalledProcessError
import tempfile

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
    assert shutdown_temp_celsius >= report_temp_celsius

    tmp_dir = tempfile.gettempdir()
    #last_report_file = 

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
'''
        if temp_c >= report_temp_celsius:
            message = str(datetime.now()) + '\n\n' + hddtemp_out
            send_email(subject='WARNING! High NAS drive temperatures!',
                message=

        import ipdb; ipdb.set_trace()
'''

    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    main()

