#!/bin/bash
# Since shell_command throws a fit when you call python3 directly for some reason, I use this script to call
# a python script indirectly. This method works well.
cd /home/homeassistant/.homeassistant/scripts
sudo /usr/bin/pkill vivaldi-bin
