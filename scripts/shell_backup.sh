#!/bin/bash
# Since shell_command throws a fit when you call python3 directly for some reason, I use this script to call
# a python script indirectly. This method works well.
cd /home/homeassistant/.homeassistant/scripts
/usr/bin/scl enable rh-python36 bash
/opt/rh/rh-python36/root/usr/bin/python3 /home/homeassistant/.homeassistant/scripts/backup.py
