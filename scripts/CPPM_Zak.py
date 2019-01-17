#!/usr/bin/python3
try:
    import requests
    import json
except Exception as e:
    print(e)

with open("../secrets.yaml") as secretFile:
  line = secretFile.readline()
  while line:
    if line.find("cppm_token") != -1:
      authToken = line.split(':')[1].strip().replace("'",'')
    elif line.find("cppm_url") != -1:
      cppm_url = line.replace("'","__").split('__')[1].strip()
    line = secretFile.readline()

url = cppm_url + 'b8d7af23e980'
headers = {
    'Content-Type': 'application/json',
    'Authorization': "{}".format(authToken)
}
try:
    r = requests.get(url, headers=headers)
except Exception as e:
    print(e)

json_r = json.loads(r.text)
online = json_r['is_online']

if online == True:
    print('On')
else:
    print('Off')
