import colorsys
import Image,ImageDraw

class Graph():
	
	def __init__(self,width,height,xmin=0,xmax=4096,ymin=0,ymax=500):
		self.im = Image.new('RGB',(width,height))
		self.draw = ImageDraw.Draw(self.im)
		self.width = width
		self.height = height
		self.xmax = xmax
		self.ymax = ymax
		self.xmin = xmin
		self.ymin = ymin
	
		self.yborder = height / 10
		self.xborder = height / 20
	
		self.gheight = height-2*self.yborder
		self.gwidth = width-2*self.xborder
		self.gxmax = width-self.xborder
		self.gymax = height-self.yborder
		if self.xmax > 0:
			self.xunit = self.gwidth / self.xmax;
		else:
			self.xunit = self.gwidth

		
	def drawLabels(self, xlabel, ylabel):
		lines = [ ylabel, "VS", xlabel ]
				
		for i in range(3):
			x = (self.width-self.draw.textsize(lines[i])[0])/2
			y = self.gymax+(i+1)*self.yborder/5
			self.draw.text((x,y),lines[i])
		
		self.draw.line((self.xborder,self.yborder,self.gxmax,self.yborder),fill=(255,0,0))
		self.draw.line((self.xborder,self.gymax+1,self.gxmax,self.gymax+1),fill=(255,0,0))
		self.draw.line((self.xborder,self.yborder,self.xborder,self.gymax+1),fill=(255,0,0))
		self.draw.line((self.gxmax,self.yborder,self.gxmax,self.gymax+1),fill=(255,0,0))
	
	def save(self,filename):
		self.im.save(filename,"BMP")

	def gridline(self,y,s=""):
		if (s==""):
			s = str(y)
		sl = self.draw.textsize(s)
		imy = self.gymax - (self.gheight * float(y) / self.ymax)
		self.draw.line((self.xborder-5, imy, self.gxmax, imy), fill=(200,200,200))
		self.draw.text((self.xborder-10 - sl[0], imy-sl[1]/2), s, fill=(255,255,255))


	def graphBar(self,x,y):
		if (self.ymax == self.ymin):
			return
		if (x > self.xmax or y > self.ymax or x < self.xmin or y < self.ymin):
			print "Bad graph point:"
			print x,y
			#return
		imx = self.xborder + self.gwidth * float(x) / self.xmax
		imy = self.gymax - max(1,self.gheight * y / self.ymax)
		#print x, imx, imy
		self.draw.rectangle((imx,imy,imx+self.xunit-0.5,self.gymax),fill=(255,255,255))
		
	def graphColorBar(self,x,y,colors):
		if (self.ymax == self.ymin):
			return
		if (x > self.xmax or y > self.ymax or x < self.xmin or y < self.ymin):
			print "Bad graph point:"
			print x,y
			#return
		n = len(colors)			# the bar will be divided into n blocks of color.
		
		if (n==0):
			return
		colors.sort()
		imx = self.xborder + self.gwidth * float(x) / self.xmax
		imx2= self.xborder + self.gwidth * float(x+1) / self.xmax - 1
		imy = self.gymax - (self.gheight * float(y) / self.ymax)
		k = (self.gymax-imy)/n
		for i in range(n):
			#print x, imx, imy
			(r,g,b) = colorsys.hsv_to_rgb(colors[i],1,1)
			self.draw.rectangle((imx,imy+i*k,imx2,imy+(i+1)*k),fill=(int(255*r),int(255*g),int(255*b)))
			
	
		