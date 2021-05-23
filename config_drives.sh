#!/usr/bin/env bash

# Use `sudo hdparm -B /dev/sd[a-f]` to print the current values for all of the
# drives. 1 is the lowest power setting.

# TODO share definition of which drives to operate on w/ spindown script

# This should be the most aggressive power saving setting, leading to more
# automatic spindowns hopefully. B127 is apparently the higest that still allows
# spindown (ref?). 254 is the most power hungry setting, with 255 completely
# disabling this type of power management, on drives which support it.
sudo hdparm -B1 /dev/sd[a-f]
