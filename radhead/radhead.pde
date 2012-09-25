// this version changes the bins array to 8192 bytes instead of 4096 two-byte "shorts"

import processing.serial.*;
Serial myPort;      // The serial port

boolean autoUpdate = false;
boolean readData = false;
boolean requestDraw = false;
boolean zoom = false;
boolean logscale = false;
int xoffset = 0;
int writeIdx = 0;
int byteIdx = 0;
int data[];
int bins[];
int numbins = 8192;
int maxcount;
int markers = 100; // opposite color every x number of bins

void setup() {
  size(1000, 600);
  frame.setResizable(true);
  println(width);
  colorMode(HSB);
  data = new int[numbins];
  bins = new int[numbins];
  maxcount = 0;
  // List all the available serial ports:
  println(Serial.list());

  // I know that the first port in the serial list on my mac
  // is always my  FTDI adaptor, so I open Serial.list()[0].
  // In Windows, this usually opens COM1.
  // Open whatever port is the one you're using.
  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 115200);

  background(0);
}

void keyPressed() {
  if (key == 'z') {
    zoom = !zoom;
    requestDraw = true;
  }
  else if ( key == 's') {
    logscale = !logscale;
    requestDraw = true;
  }
  else if (keyCode == LEFT) {
    xoffset -= 50;
    xoffset = max(xoffset, 0);
    requestDraw = true;
  }
  else if (keyCode == RIGHT ) {
    xoffset += 50;
    xoffset = min(xoffset, numbins-width);
    requestDraw = true;
  }
  else if (key == '0' || key == '1' || key == '2' || key == '3' || key == '4' || key == '5' || key == '6' || key == '7' || key == '8' || key == '9' || keyCode == ENTER) {
    myPort.write(key);
  }
}

void draw() {  
  if (requestDraw) {
    print("draw");
    background(0);
    if (maxcount > 0) {      
      noStroke();
      for (int i = 0; i < numbins; ++i) {
        int val = bins[i];
        int x = i * width / numbins;
        if (zoom) {
          x = i - xoffset;
          if (x < 0 || x > width)
            continue;
        }
        int w = ((i - xoffset + 1) * width / numbins - x);
        int h = val * height / maxcount;
        if (logscale) {
          h = int(log(val) * height / log(maxcount));
        }
        int y = height - h;
        if (i % markers == 0) {
          fill(256-256*i/numbins, 255, 255);
        } 
        else {
          fill(256*i/numbins, 255, 255);
        }
        rect(x, y, max(1, w), h);
      }
    }
    requestDraw = false;
  }

  while (myPort.available () > 0) {
    int inByte = myPort.read();
    if (readData) {
      data[writeIdx] = inByte;
      //println(byteIdx);
      //println(bins[writeIdx]);

      ++writeIdx;

      if (writeIdx > 8191) {
        readData = false;
        requestDraw = true;
        print("stop");

        maxcount = 0;
        for (int i = 0; i < numbins; ++i) {
          //          int idx = i*2;
          //          int val = data[idx] + (data[idx+1]<<8);
          bins[i] += data[i];
          if (bins[i] > maxcount)
            //         if (bins[i] - maxcount < maxcount)
            if (i < 8191) maxcount = bins[i];
        }
      }
    } 
    else if (inByte == 'r') {
      print("start");
      readData = true;
      writeIdx = 0;
      byteIdx = 0;
    } 
    else if (inByte == '=') {
      print("   count = ");
      println(myPort.readStringUntil(13));
    }
  }
}
/*
void saveData() {
 File f = open("data.txt");
 }
 */
