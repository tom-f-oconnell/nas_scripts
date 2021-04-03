#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Pass one drive device (e.g. /dev/sda) to check the testing status of"
    exit 1
fi

sudo smartctl -a $1 | grep -i 'self-test execution status:' -A 1
