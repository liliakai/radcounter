import sys


def run(filename):

	f = open(filename)
	counts = 0;
	minutes = 0;
	largest = 0;
	
	bins = {}

	print("scanning for largest ADC value")	
	while True:
		line = f.readline()
		if (len(line) < 2):
			break
		if not line.startswith("time"):
			data = int(line)
			if largest < data:
				largest = data

	print("binning events")	
	f.seek(0)
	while True:
		line = f.readline()
		if (len(line) < 2):
			break
		if line.startswith("time"):
			minutes = minutes + 1
			print str(minutes) + " min"
			continue
		data = int(line)
		binNum = 4096 * data / largest
		if bins.has_key(binNum):
			bins[binNum] = bins[binNum] + 1
		else:
			bins[binNum] = 1	
			
			counts = counts+1
			print str(data)
			
	
	outputFilename = filename.split(".")[0] + "_bins.txt";
	fbin = open(outputFilename,'w')
	keys = bins.keys()
	keys.sort()
	for key in keys:
		fbin.write(str(key) + " " + str(bins[key]) + "\n")
	fbin.close()
	
	
	if (minutes > 0):
		print "avg cpm: " + str(counts/minutes)
		
	return outputFilename
		

if __name__ == "__main__":
	if ( len(sys.argv) > 1):
		filename = sys.argv[1]
		run(filename)
	else:
		exit()
