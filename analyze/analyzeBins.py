import sys
import math
from PIL import Image,ImageDraw

def run(filename):

	f = open(filename)

	bins = {}
	binCount = 0
	maxBinValue = 0
	maxBinNum = 0

	for line in f:
		binCount = binCount+1
		data = line.split()
		bin = int(data[0])
		value = int(data[1])
		bins[bin] = value
		if (value > maxBinValue):
			maxBinValue = value

	keys = bins.keys()
	keys.sort()
	maxBinNum = keys[len(keys)-1]
	print keys

	print maxBinValue
	im = Image.new('RGB',(4096,maxBinValue+1))
	draw = ImageDraw.Draw(im)

	for key in keys:
		draw.line((key,maxBinValue,key,maxBinValue-bins[key]),fill=(255,255,255))

	print filename
	print "Non-empty bins:\t" 		+ str(binCount)
	print "Biggest bin value:\t" 	+ str(maxBinValue)
	print "Biggest bin number:\t" 	+ str(maxBinNum)

	im.save(filename.split(".")[0]+".bmp","BMP")

	#width = maxBinNum
	width = 1000
	height = 1000
	im = Image.new('RGB',(width,height))
	draw = ImageDraw.Draw(im)

	xunit = width / maxBinNum;
	yborder = height / 10
	xborder = height / 20

	maxlogval = math.log(maxBinValue)

	h = height-yborder
	w = width-2*xborder
	xmax = width-xborder
	for key in keys:
		x = xborder + w * float(key) / maxBinNum
		y = h * math.log(bins[key]) / maxlogval

		print key, x, y

		draw.rectangle((x,h-y,x+xunit,h),fill=(255,255,255))

	#draw.line((xborder,0,xmax,0),fill=(255,0,0))
	draw.line((xborder,h,xmax,h),fill=(255,0,0))
	draw.line((xborder,0,xborder,h),fill=(255,0,0))
	draw.line((xmax+xunit,0,xmax+xunit,h),fill=(255,0,0))


	draw.text((xborder,h+yborder/5),"x: 0 -> %d" % maxBinNum)
	draw.text((xborder,h+yborder/5*2),"y: 1 -> %d (log scale)" % maxBinValue)
	im.save(filename.split(".")[0]+"_log.bmp","BMP")



if __name__ == "__main__":
	filename = "./bindata.txt"
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		run(filename)
