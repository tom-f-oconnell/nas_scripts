#!/usr/bin/env bash


# Unless zpool is set up to use IDs, this may be necessary to make
# pools reliably get mounted on boot:
# sudo zpool export <poolname>
# sudo zpool import -d /dev/disk/by-id <poolname>

# This and the hdparm stuff got from here,
# https://rudd-o.com/linux-and-free-software/tip-letting-your-zfs-pool-sleep
sudo zfs set atime=off nas

# TODO maybe use a higher apm? not sure if this will cause the drive to sleep
# much faster than the spindown time... why even use apm if spindown already
# accomplishes what i want (provided apm is in the range that allows spindown)?

# Edit /etc/hdparm.conf as sudo, and for each drive (/dev/disk/by-id/...)
# under zpool status <poolname>, add an entry like this:
# /dev/disk/by-id/<drive-id> {
#     spindown_time = 12
#     apm = 1
# }

