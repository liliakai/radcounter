#!/usr/local/bin/python
# radcount.py
import sys

sys.path.append("/home/lilia/Imaging-1.1.7/build/lib.freebsd-8.2-RELEASE-i386-2.6")
sys.path.append("/home/lilia/rad")

import processData
import analyzeBins

if __name__ == "__main__":
	if ( len(sys.argv) > 1):
		filename = sys.argv[1]
		binFileName = processData.run(filename)
		analyzeBins.run(binFileName)
	else:
		exit()
