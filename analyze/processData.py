import sys


def run(filename):

	f = open(filename)
	counts = 0;
	minutes = 0;

	bins = {}

	while True:
		bytes = f.read(2)
		if (len(bytes) < 2):
			break

		data = (ord(bytes[0]) << 8) + ord(bytes[1])

		if (data == 0xffff):
			minutes = minutes + 1
			print str(minutes) + " min"
		else:
			binNum = 4096 * data / 0xffff
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
