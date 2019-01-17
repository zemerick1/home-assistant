#!/usr/bin/python3
file = open("/home/homeassistant/.homeassistant/backup.last", 'r')
last_backup = file.read().replace('\n', '')
print(last_backup)
