#!/usr/bin/env bash

# https://linuxconfig.org/how-to-configure-smartd-and-be-notified-of-hard-disk-problems-via-email

sudo apt-get update
sudo apt-get install smartmontools msmtp msmtp-mta

# TODO copy etc-msmtprc to /etc/msmtprc, change permission to 644, and fill in
# placeholder values for username / password w/ values in gmail_credentials.txt
# (kept out of source control)

