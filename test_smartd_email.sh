#!/usr/bin/env bash

# If each line in /etc/smartd.conf has '-M test', a test email will be sent when
# the daemon restarts.
sudo systemctl restart smartd
