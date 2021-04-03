#!/usr/bin/env bash

./list_zpool_devices.py | xargs -L 1 -i sh -c 'echo {}; ./smart_test_status.sh {}'
