#!/usr/bin/python
import os
import time
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

def parse_packet(packet):
  length = len(packet)
  result = 0
  for i in range(length):
    result |= (packet[length - 1 - i] & 0x7F) << 7*i
  return result

def read_packet(port):
  while True:
    data = ord(port.read(1))
    if (data & 0x80) != 0:
      packet = [data] + map(ord, port.read(2))
      return parse_packet(packet)

def main():
  outfile = open_file()
  port = open_serial()

  lasttime = time.time()
  count = 0
  while True:
    outfile.write(str(read_packet(port)))
    outfile.write('\n')
    count += 1
    if time.time() - lasttime  > 60:
      lasttime = time.time()
      outfile.write('time ')
      outfile.write(str(int(time.time())))
      outfile.write('\n')
      print count
      count = 0
    outfile.flush()

  outfile.close()
  port.close()

if __name__ == "__main__":
  main()
