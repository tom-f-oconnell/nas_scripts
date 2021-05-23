#!/usr/bin/env bash

echo "active/idle = spinning"
echo "standby OR sleeping = not spinning"

# The output will have information on whether drives are currently spinning or
# not. From hdparm man page, possible states are:
# - active/idle (normal operation)
# - standby (low power mode, drive has spun down)
# - sleeping (lowest power mode, drive is completely shut down)
# - unknown (drive does not support this command)
sudo hdparm -C /dev/sd[a-f]
