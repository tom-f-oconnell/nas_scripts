#!/usr/bin/env bash

# TODO share definition of which drives to operate on w/ spindown script

# This should be the most aggressive power saving setting, leading to more
# automatic spindowns hopefully. B127 is apparently the lowest that still allows
# spindown. 254-255 the max, with 255 completely disabling this type of power
# management, on drives which support it.
# TODO test this works. made this script after i actually set them originally.
sudo hdparm -B1 /dev/sd[a-f]
