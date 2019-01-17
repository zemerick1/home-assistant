'''
Created by zemerick
Offloads homeassistant home directory to 'backup_server' located in secrets.yaml
Leaves behind backup.last file that I use via last_backup.py to build last backup sensor
'''
import glob
import datetime
from zipfile import ZipFile
import os
import pysftp

fdateTime = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
backupFile = 'backup_{}.zip'.format(fdateTime)
files = glob.glob('/home/homeassistant/.homeassistant/**/*.*', recursive=True)

with ZipFile(backupFile, 'w') as zip_f:
    for file in files:
        # Skip Audio files. . we don't care.
        if file.endswith('.mp3'):
          print('Skipping Google Audio file: {}'.format(file))
        else: 
          # Add files to zip archive.
          print('Adding file: {0} to {1}'.format(file, backupFile))
          zip_f.write(file)


# SFTP stuff
# Auto accept hostKey from server.
connOpts = pysftp.CnOpts()
connOpts.hostkeys = None

# Bring in external creds
with open("../secrets.yaml") as secretFile:
  line = secretFile.readline()
  while line:
    if line.find("backup_server") != -1:
      secret = line.split(':')[1].strip()
      backup_server = secret
    elif line.find("backup_user") != -1:
      secret = line.split(':')[1].strip()
      backup_user = secret
    elif line.find("backup_pass") != -1:
      secret = line.split(':')[1].strip()
      backup_pass = secret
    line = secretFile.readline()

# Make connection to server
server = pysftp.Connection(host=backup_server, username=backup_user, password=backup_pass, cnopts=connOpts)
server.chdir('/mnt/HD/HD_a2/zemerick/homeassist')

# Attempt upload to backup server
try:
    print('Uploading {} to server'.format(backupFile))
    server.put(backupFile)
except Exception as e:
    print(e)

# Remove original backup.
os.remove(backupFile)

# Close connection to server
server.close()

# Create file to track last backup
if os.path.isfile("../backup.last"):
	os.remove("../backup.last")
f = open("../backup.last", "w+")
f.write(fdateTime)
f.close
