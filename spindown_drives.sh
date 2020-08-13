#!/usr/bin/env bash

# Using a range rather than ? wildcard to exclude the OS drive.
sudo hdparm -y /dev/sd[a-f]
