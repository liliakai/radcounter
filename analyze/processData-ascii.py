import sys
import time
import graph
from PIL import Image,ImageDraw

def scaled_value(data, smallest, largest):
  (data - smallest) / float(largest)

def run(filename):

  f = open(filename)
  counts = 0;
  minutes = 0;
  now = 0;
  largest = 0;
  smallest = 0xFFFFFF
  bins = {}
  start = 0;
  cpm = []
  maxcpm = 0;
  lastcount = 0
  minuteData = []

  print("scanning for largest ADC value")
  while True:
    line = f.readline().strip()
    if (len(line) < 2):
      break
    if not line.startswith("time"):
      data = int(line)
      if largest < data:
       largest = data
      if smallest > data:
        smallest = data
    datarange = largest - smallest
  print 'largest %d' % largest
  print 'smallest %d' % smallest

  print("binning events")
  f.seek(0)
  while True:
    line = f.readline()
    if (len(line) < 2):
      break
    if line.startswith("time"):
      minutes = minutes + 1
      diff = counts - lastcount
      cpm.append(minuteData)
      if len(minuteData) > maxcpm:
        maxcpm = len(minuteData)
      minuteData = []
      lastcount = counts
      print str(minutes) + " min (" + line.strip() + ")"
      continue
    data = int(line)
    minuteData.append(data)
    binNum = int(4096 * data / float(0x1FFFFF))
    if bins.has_key(binNum):
      bins[binNum] = bins[binNum] + 1
    else:
      bins[binNum] = 1
    counts = counts+1

  outputFilename = filename.split(".")[0] + "_bins.txt";
  fbin = open(outputFilename,'w')
  print("Duration: %d minutes\n" % minutes);
  if minutes > 0:
    print("Counts: %d (%f CPM)\n" % (counts, counts/minutes));
  else:
    print("Counts: %d (%f CPM)\n" % (counts, counts));

  keys = bins.keys()
  keys.sort()
  for key in keys:
    fbin.write(str(key) + " " + str(bins[key]) + "\n")
  fbin.close()

  g = graph.Graph(1000,1000,0,minutes,0,maxcpm)
  for t in range(minutes):
    #g.graphBar(t,cpm[t])
    #print len(cpm[t])
    g.graphColorBar(t,len(cpm[t]),[float(f-smallest)/float(datarange) for f in cpm[t]])
  timestamp = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(start))
  xlabel = "time (min) since %s [%d,%d]" % (timestamp,0,minutes)
  ylabel = "pulses recorded [%d,%d]" % (0,maxcpm)
  g.drawLabels(xlabel, ylabel)
  g.save(filename.split(".")[0]+"_timeline.bmp")
  if (minutes > 0):
    print "avg cpm: %f" % (float(counts)/minutes)
    print "max cpm: %d" % (maxcpm)
  return outputFilename

if __name__ == "__main__":
  if ( len(sys.argv) > 1):
    filename = sys.argv[1]
    run(filename)
  else:
    exit()
