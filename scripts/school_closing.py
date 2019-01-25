#!/usr/bin/python3
'''
Scrapes local news website to see if school is closed.
'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Get configuration Items (don't want to expose county to the internet!)
with open("/home/homeassistant/.homeassistant/secrets.yaml") as secretFile:
  line = secretFile.readline()
  while line:
    if line.find("school_county:") != -1:
      findCounty = line.split(':')[1].strip().replace("'",'')
    elif line.find("school_url") != -1:
      school_url = line.replace("'","__").split('__')[1].strip()
    line = secretFile.readline()

url = school_url

r = requests.get(url)

r_html = r.text
soup = BeautifulSoup(r_html, 'html.parser')
# kill all script and style elements
for script in soup(["script", "style"]):
    script.decompose()    # rip it out


# find the appropriate tags and parse them until we find our school.
for county in soup.find_all("article",class_="closing js-block"):
    # Find our county
    foundCounty = county.findChildren()[0].getText()
    if foundCounty == findCounty:
        # Grab the reason
        reason = county.findChildren()[1].getText()
        # Grab time so we don't act on stale data
        closeTime = county.findChildren()[2].getText()
        break

if reason is None: # May use this in the future. (JSON)
    reason = 'No reason given.'

# Convert our string to dateTime object
closeTime = closeTime.split('T')[0]
closeTime = datetime.strptime(closeTime,'%Y-%m-%d')
if closeTime > datetime.now():
    updatedTime = True

if updatedTime and foundCounty == findCounty:
    print('Closed')
else:
    print('Open')