#!/usr/bin/python3
'''
This utilizes Clearpass NAC from Aruba to identify if a client is online by MAC address.
It queries the Insight database for offline/online status via RADIUS accounting messages.
I then use a binary_sensor command line to pull this data for presence detection.
'''
try:
    import requests
    import json
except Exception as e:
    print(e)
with open("../secrets.yaml") as secretFile:
  line = secretFile.readline()
  cnt = 1
  while line:
    if line.find("cppm_token") != -1:
      authToken = line.split(':')[1].strip().replace("'",'')
    elif line.find("cppm_url") != -1:
      cppm_url = line.replace("'","__").split('__')[1].strip()
    line = secretFile.readline()

url = cppm_url + '1098c306d3ba'
print(url)
print("token: {}".format(authToken))
headers = {
    'Content-Type': 'application/json',
    'Authorization': "{}".format(authToken)
}
try:
    r = requests.get(url, headers=headers)
except Exception as e:
    print(e)

json_r = json.loads(r.text)
print(json_r)
online = json_r['is_online']

if online == True:
    print('On')
else:
    print('Off')
