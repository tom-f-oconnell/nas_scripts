
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
`gmail_credentials.txt` file. `/etc/msmtprc` should have `644` permissions, but
this seemed to be the default for me anyway.

Note that the current `smartd` configuration does a short test every day between
4-5am and a long test Saturdays between 5-6am (duplicated from my comment in
`etc-smartd.conf`. The long test especially, however, may take more than 1hr?
Not sure.

To test that the email setup worked correctly:
```
./test_smartd_email.sh
```
You should receive an email to the same account that was set up as the sender.


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


### Monitoring the IO to the ZFS filesystem

To get a summary of all IO since boot, for each drive:
```
sudo zpool iostat -v
```

To measure in 5 second intervals:
```
sudo zpool iostat -v -y 5
```

Note that `zpool iostat` [does not seem to have](http://manpages.ubuntu.com/manpages/impish/man8/zpool-iostat.8.html)
any options for actually breaking this IO down by processes.


### Get hard drive temperatures

To list hard drive temperatures (without also checking against thresholds
and taking action like `check_temperatures.py`):
```
sudo hddtemp /dev/sd?
```


### Trying to get the drives to spin down

To check whether drives are spun down (and which, because they don't all seem to
always spin down at the same time):
```
./check_drive_powermodes.sh
```

To force drives to spin down:
```
./spindown_drives.sh
```

#### Determining what is using the ZFS filesystem

```
sudo fuser -mv /nas
```

Above should be sufficient, but this might be more useful in some circumstances:
```
sudo lsof +f -- /nas
```

Yet even with `sudo hdparm -B /dev/sd[a-f]` showing all 1s (which should be the
power management setting where the drives spin down the most), and the output of
the above two commands being essentially empty, many / all of the drives are not
consistently spinning down.

In testing when nothing seemed to be using `/nas`, I got both of these outputs
on different attempts a few minutes apart:

The kernel lines in these outputs might or might not have something to do with
the drives not spinning down.
```
tom@nas:~$ sudo fuser -mv /nas
                     USER        PID ACCESS COMMAND
/nas:                root     kernel mount /nas
                     root     kernel knfsd /nas
```

```
tom@nas:~$ sudo fuser -mv /nas
                     USER        PID ACCESS COMMAND
/nas:                root     kernel mount /nas
```

The `knfsd` entry above will definitely appear if I do mount this filesystem via
NFS on my desktop, and it seems to stay for at least a little while after. I
didn't intentionally have the NAS mounted via NFS during the above test, but a
`find / ...` command (on my desktop) might have looked in `~/nas` briefly and
triggered the auto mount?

A similar line will also appear from mounting (until when?) running `fuser` on
my desktop:
```
tom@blackbox:~$ sudo fuser -mv /mnt/nas
                     USER        PID ACCESS COMMAND
/mnt/nas:            root     kernel mount /mnt/nas
```

`lsof` doesn't seem to work as nicely from my desktop, producing output like
this:
```
tom@blackbox:~$ sudo lsof +f -- /mnt/nas
lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1000/gvfs
      Output information may be incomplete.
```


### Hardware

- Motherboard: Supermicro X11SSM-F
  - From `sudo dmidecode -t 2`

  - There are 3 ethernet ports on this motherboard, and the docs say that the
    one by itself (towards top of case), is "Dedicated IPMI LAN", so I'm
    thinking that one might not be the main one I want to use. If I want to try
    IPMI at some point, but don't want an extra cable,
    [this might be useful](https://serverfault.com/questions/361940).

  - LGA1151 socket

  - Supports ECC RAM, which is a big thing I was looking for, as it's often
    recommended in discussions of building machines for use as a NAS with ZFS.


- HDDs for ZFS pool: 6x Hitachi HUS72403 (3TB)
  - `/dev/sd[a-f]`
  - Total capacity ends up being ~11TB in raidz2 configuration
  - From `sudo lshw -C disk`


- USB drive with OS installed on it: SanDisk Cruzer Fit (15GB)
  - Connected to motherboard internally
  - Should be `/dev/sdg`
  - From `sudo lshw -C disk`
  - Unclear if this can meaningfully be checked with `smartctl`, and it's not
    worth the effort in trying to figure that out. Should just upgrade to a
    proper SSD if I care.

- CPU: Intel Pentium G4560
  - From `sudo lshw -C cpu`

- Memory: Kingston 9965643-006.A01G 2400 MHz w/ ECC (8GB)
  - From `sudo lshw -C memory`

