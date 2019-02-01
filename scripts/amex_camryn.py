#!/usr/bin/python3
'''
Reads data from amex.last to get account values.
'''
file = open("/home/homeassistant/.homeassistant/amex.last", 'r')
camryn = file.readlines()[1].replace('\n', '').replace('$','')
file.close()
print(camryn)
