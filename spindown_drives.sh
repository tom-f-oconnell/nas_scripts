#!/usr/bin/env bash

# TODO maybe add some kind of cron job that does this periodically (if there are
# no current processes using the /nas filesystem)?

# Using a range rather than ? wildcard to exclude the OS drive.
sudo hdparm -y /dev/sd[a-f]
