#!/usr/bin/python3
from datetime import *
import sys

sys.argv.append(sys.argv[1].split('.')[0] + '_JST.' + sys.argv[1].split('.')[1])
fs = open(sys.argv[1], 'r')
fd = open(sys.argv[2], 'w')
line = fs.readline()
word = line.split(',')
line = ','.join([ word[0], '<YYYY-MM-DD hh:mm:ss>', word[3], word[4], word[5], word[6] ])
fd.write(line)

for line in fs:
    word = line.split(',')
    date = word[1]
    time = word[2]
    date_time = datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), int(time[:2]), int(time[2:4]), int(time[4:6])) + timedelta(hours=8)
    line = ','.join([ word[0], str(date_time), word[3], word[4], word[5], word[6] ])
    fd.write(line)

fs.close()
fd.close()

