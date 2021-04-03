#!/usr/bin/env python3

"""
Lists devices (e.g. /dev/sda) for each drive in the pool with the name passed as
argument (or 'nas' by default).
"""

import argparse
import subprocess as sp
from os.path import join, realpath


def get_pool_devices(pool_name='nas'):
    """Returns a list of paths to devices (e.g. /dev/sda) in the ZFS pool.
    """
    p = sp.run(['zpool', 'status', pool_name], check=True, stdout=sp.PIPE)
    lines = p.stdout.decode('utf-8').splitlines()
    # a '\t' character and 4 spaces
    drive_line_n_leading_whitespace_chars = 5

    device_paths = []
    for x in lines:
        # Might be more robust to look for lines in relation to the line w/
        # parts NAME/STATE/READ/WRITE/CKSUM, or maybe look for lines between
        # empty lines that have maximum left whitespace, but as long as this
        # works...
        n_leading_whitespace_chars = len(x) - len(x.lstrip())

        if n_leading_whitespace_chars == drive_line_n_leading_whitespace_chars:
            parts = x.split()
            assert len(parts) == 5
            drive_id = parts[0]
            device_paths.append(realpath(join('/dev/disk/by-id', drive_id)))

    return device_paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', nargs='?', default='nas', help='name of pool to'
        ' list devices for'
    )
    args = parser.parse_args()

    devices = get_pool_devices(args.name)
    for d in devices:
        print(d)


if __name__ == '__main__':
    main()

