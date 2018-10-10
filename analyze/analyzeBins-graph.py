import sys
import math
import graph
from PIL import Image,ImageDraw

def run(filename):

	f = open(filename)

	bins = {}
	binCount = 0
	maxBinValue = 0
	mbvIndex= 0
	maxBinNum = 0
	lastBinOver10 = 0
	print f.readline().strip()
	print f.readline().strip()
	print f.readline().strip()
	for line in f:

		binCount = binCount+1
		data = line.split()
		bin = int(data[0])
		value = int(data[1])
		bins[bin] = value
		if (value > maxBinValue):
			maxBinValue = value
			mbvIndex = bin
		if (value > 10):
			lastBinOver10 = bin

	keys = bins.keys()
	keys.sort()
	if len(keys) > 0:
		maxBinNum = keys[len(keys)-1]
	else:
		maxBinNum = -1
	#print keys
	#print maxBinValue
	print filename
	print "Non-empty bins:\t%d" % (binCount)
	print "Highest bin:\t%d" % (maxBinNum)
	print "Fullest bin:\t%d (%d counts)" % (mbvIndex,maxBinValue)

	g = graph.Graph(4196,1000,0,4096,0,maxBinValue)
	for key in keys:
		#g.graphBar(key,bins[key])
		g.graphColorBar(key,bins[key],[float(key)/4096])
	g.drawLabels("adc reading [0,4096]", "total counts [1,%d]" % maxBinValue)
	g.save(filename.split("_")[0]+"_linearspectrum.bmp")


	if maxBinValue > 0:
		g = graph.Graph(4196,1000,0,4096,0,math.log(maxBinValue))
	else:
		g = graph.Graph(4196,1000,0,4096,0,1)

	gridline = 1
	while( gridline <= 10 and gridline < maxBinValue):
		g.gridline(math.log(gridline),str(gridline))
		tmp = gridline
		while( gridline < maxBinValue ):
			g.gridline(math.log(gridline),str(gridline))
			gridline *= 10

		gridline = tmp+1

	for key in keys:
		value = bins[key]
		#g.graphBar(key,math.log(value))
		if key > 2044:
			tmp = math.log(max(1,0.25*value))
			for i in range(4):
				#g.graphBar(key+i,tmp)
				g.graphColorBar(key+i,tmp,[float(key+i)/4096])
		elif key > 1022:
			tmp = math.log(max(1,0.5*value))
			for i in range(2):
				#g.graphBar(key+i,tmp)
				g.graphColorBar(key+i,tmp,[float(key+i)/4096])
		else:
			#g.graphBar(key,math.log(value))
			g.graphColorBar(key,math.log(value),[float(key)/4096])

	g.drawLabels("adc reading [0,4096]", "total counts [1,%d]" % maxBinValue)
	g.save(filename.split("_")[0]+"_logspectrum.bmp")




if __name__ == "__main__":
	filename = "./bindata.txt"
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		run(filename)
