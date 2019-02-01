#!/usr/bin/python3
'''
Reads data from amex.last to get account values.
'''
file = open("/home/homeassistant/.homeassistant/amex.last", 'r')
chelsea = file.readlines()[0].replace('\n', '').replace('$','')
file.close()
print(chelsea)
