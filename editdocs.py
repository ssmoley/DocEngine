import os
import subprocess
import glob

files = glob.glob('c:\\users\\sean\\desktop\\python\\*.txt')
complete = []
s = ''
i = 0

f = open('complete.txt', 'r+')
for line in f:
    complete.append(line.strip())
    print line.strip()
f.close()

for item in files:
    if complete.count(item) == 0:
        subprocess.call('notepad.exe %s' % item)
        print 'count , Run Notepad %s' % item
        complete.append('%s\n' % item)
        i = +i
    s = raw_input('Keep Going?')
    if s != '':
        break
    else:
        continue


f = open('complete.txt', 'w+')
for item in complete:
    f.write('%s\n' % item)

f.close()
