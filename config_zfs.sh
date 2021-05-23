#!/usr/bin/env bash


# Unless zpool is set up to use IDs, this may be necessary to make
# pools reliably get mounted on boot:
# sudo zpool export <poolname>
# sudo zpool import -d /dev/disk/by-id <poolname>

# These properties seem to be persistant across boots and stuff, so this should
# only be necessary once on pool setup? Not 100% sure...
# Either way, this link had some ways to check current status of this property:
# https://www.unixtutorial.org/zfs-performance-basics-disable-atime/
# Though strangely, despite running the command below (setting `atime=off`),
# there is no output when I run `sudo zpool get all | grep time`.
# However the other method in the same link, `mount | grep nas`, seems to
# indicate atime is currently off whether or not it was on initially, because
# the output was `nas on /nas type zfs (rw,noatime,xattr,noacl)` (includes
# `noatime`).

# This and the hdparm stuff got from here,
# https://rudd-o.com/linux-and-free-software/tip-letting-your-zfs-pool-sleep
# TODO was this supposed to be a one time thing or supposed to be run per boot?
# Properties like these seem to be 
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

