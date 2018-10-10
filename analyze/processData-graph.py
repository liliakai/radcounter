import sys
import time
import graph
from PIL import Image,ImageDraw

def run(filename):

	f = open(filename)
	counts = 0;
	minutes = 0;
	now = 0;
	bins = {}
	start = 0;
	cpm = []
	maxcpm = 0;
	lastcount = 0
	minuteData = []
	while True:
		bytes = f.read(2)
		if (len(bytes) < 2):
			break

		data = (ord(bytes[0]) << 8) + ord(bytes[1])
		if (data == 0xffff):
			diff = counts - lastcount
			cpm.append(minuteData)
			if len(minuteData) > maxcpm:
				maxcpm = len(minuteData)
			minuteData = []
			lastcount = counts
			minutes = minutes + 1
			#print "min %d, %d counts of %d" % (minutes, diff, counts)
			bytes = f.read(4)
			if len(bytes) == 4:
				data = (ord(bytes[0])<< 24) + (ord(bytes[1])<<16) + (ord(bytes[2]) << 8) + ord(bytes[3])
				now = data
				#print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(now))
				if start == 0:
					start = now
		elif data > 0x0fff:
			print "ERR! ignoring, pulse height too big: %d" % data
		else:
			minuteData.append(data)
			binNum = data #4096 * data / 0x0fff
			if bins.has_key(binNum):
				bins[binNum] = bins[binNum] + 1
			else:
				bins[binNum] = 1

			counts = counts+1
			#print str(data)

	outputFilename = filename.split(".")[0] + "_bins.txt";
	fbin = open(outputFilename,'w')
	if (now != 0):
		fbin.write(time.strftime("Start Time: %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime(start)));
	fbin.write("Duration: %d minutes\n" % minutes);
	if minutes > 0:
		fbin.write("Counts: %d (%f CPM)\n" % (counts, counts/minutes));
	else:
		fbin.write("Counts: %d (%f CPM)\n" % (counts, counts));

	keys = bins.keys()
	keys.sort()
	for key in keys:
		fbin.write(str(key) + " " + str(bins[key]) + "\n")
	fbin.close()

	#ymax = max(cpm)
	#im = Image.new('RGB',(minutes,ymax))
	#draw = ImageDraw.Draw(im)
	#for t in range(minutes):
	#	draw.line((t,ymax - cpm[t],t,ymax),fill=(255,255,255))
	#im.save(filename.split(".")[0]+".bmp","BMP")

	g = graph.Graph(1000,1000,0,minutes,0,maxcpm)
	for t in range(minutes):
		#g.graphBar(t,cpm[t])
		#print len(cpm[t])
		g.graphColorBar(t,len(cpm[t]),[float(f)/4096.0 for f in cpm[t]])
	g.drawLabels("time (min) since %s [%d,%d]" % (time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(start)),0,minutes), "pulses recorded [%d,%d]" % (0,maxcpm))
	g.save(filename.split(".")[0]+"_timeline.bmp")

	if (minutes > 0):
		print "avg cpm: %f" % (counts/minutes)
		print "max cpm: %d" % (maxcpm)

	return outputFilename


if __name__ == "__main__":
	if ( len(sys.argv) > 1):
		filename = sys.argv[1]
		run(filename)
	else:
		exit()
