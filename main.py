#!/usr/bin/python
import os
import serial

def filename(i):
  return str(i) + '.rad'

def open_serial():
  return serial.Serial('/dev/ttyUSB0', 115200)

def open_file():
  logdir = 'data'
  try:
    os.mkdir(logdir)
  except:
    pass
  files = os.listdir(logdir)

  i=0
  while (True):
    if not (filename(i) in files):
      break
    i += 1

  return open(logdir + '/' + filename(i), 'w')

def main():
  outfile = open_file()
  port = open_serial()

  while True:
    outfile.write(port.readline())

  outfile.close()
  port.close()

if __name__ == "__main__":
  main()
