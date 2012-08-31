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

def parse_packet(packet)
  length = len(packet)
  result = 0
  for i in range(length):
    byte = packet[length - 1 - i] & 0x7F
    result += packet[length - 1 - i] << 7*i
  return result

def read_packet(port)
  while True:
    data = ord(port.read(1))
    if (data & 0x80) != 0:
      packet = [data] + map(ord, port.read(2))
      return parse_packet(packet)

def main():
  outfile = open_file()
  port = open_serial()

  while True:
    outfile.write(read_packet())

  outfile.close()
  port.close()

if __name__ == "__main__":
  main()
