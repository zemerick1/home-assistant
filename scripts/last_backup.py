#!/usr/bin/python3
'''
Reads backup.last file to get date for the last backup.
A sensor is built with this data. (See backup.py)
'''
file = open("/home/homeassistant/.homeassistant/backup.last", 'r')
last_backup = file.read().replace('\n', '')
file.close()
print(last_backup)
