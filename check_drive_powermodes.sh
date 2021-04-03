#!/usr/bin/env bash

# The output will have information on whether drives are currently spinning or
# not.
sudo hdparm -C /dev/sd[a-f]
