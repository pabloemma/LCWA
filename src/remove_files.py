import os
import time
import sys

if len(sys.argv) != 2:
    print("usage", sys.argv[0], " <dir>")
    sys.exit(1)

workdir = sys.argv[1]

now = time.time()
old = now - 7 * 24 * 60 * 60

for f in os.listdir(workdir):
    path = os.path.join(workdir, f)
    if os.path.isfile(path):
        stat = os.stat(path)
        if stat.st_ctime < old:
            print ("removing: ", path)
            # os.remove(path) # uncomment when you will sure :)