#!/usr/bin/python3
file = open("/sys/class/thermal/thermal_zone0/temp", 'r')
c_temp = int(file.read(5))
c_temp = c_temp * 0.001

f_temp = round((c_temp * (9/5)) + 32, 2)

print(f_temp)
