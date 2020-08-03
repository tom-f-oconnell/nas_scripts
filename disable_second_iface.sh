#!/usr/bin/env bash

# ifconfig
# (in output, eno1 has IP address and eno2 does not)
# TODO is this only true because i executed the commands below?
# also, there are still 2 IP addresses for this computer, according to pfsense.
# any way to fix that?

# systemctl | grep eno2
# (pfsense still seems to recognize it though, as it it gives it a DHCP lease,
# and i can ping it from other computers on the lan...)
sudo systemctl disable sys-devices-pci0000:00-0000:00:1d.1-0000:03:00.0-net-eno2.device
sudo systemctl disable sys-subsystem-net-devices-eno2.device
