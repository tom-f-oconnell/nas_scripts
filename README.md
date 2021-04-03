
### Setup

To make your drives spindown as much as possible (which I wanted for noise
reasons), run:
```
./config_drives.sh
```

To set up the automated notifications provided by `check_temperatures.py` and
`smartd`, you will need to generate an app-specific password for a Gmail account
of yours. Save the username (excluding the `@gmail.com` part) and *app-specific*
password to a file in this directory called `gmail_credentials.txt`, with the
username on the first line and the password on the second line.

To setup SMART harddrive health monitoring:
```
./setup_smart_alerting.sh
```
...then copy `etc-smartd.conf` and `etc-msmtprc` to `/etc/smartd.conf` and 
`/etc/msmtprc`, respectively, and manually change `GMAIL_USER` and `PASSWORD`
placeholders in both to the corresponding values you saved to the
`gmail_credentials.txt` file.


To setup temperature monitoring/alerting/automatic shutdown:
```
./setup_temperature_alerting.sh
```

To change the thresholds for either sending emails or shutting down the machine,
edit `check_temperatures.py` to change `hdd_[report|shutdown]_temp_celsius`.


#### TODO

- Complete these instructions

- Was my current NAS set up using `~/ansible-nas`? and would I want to use
  that again in the future? I vaguely recall it doing more than I wanted...
  I don't recall if I actively had to undo anything it did...


### ZFS commands

Using `nas` as the name of the pool in the commands below.

Initiate a scrub:
```
sudo zpool scrub nas
```
Note that something it seems `scrub` has currently already been set up to run
the second Sunday of every month, as you can see by:
```
cat /etc/cron.d/zfsutils-linux
```
Though I'm not sure what set this up, and if I continue to only sporadically
power on my NAS, it may not be triggered very often.


Check the progress of an ongoing scrub:
```
zpool status -v nas
```


### Hard drive monitoring

To list hard drive temperatures (without also checking against thresholds
and taking action like `check_temperatures.py`):
```
sudo hddtemp /dev/sd?
```
