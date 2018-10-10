Radcounter
==========
Yet another iteration of our home-made radiation spectrometer.

Hardware
--------
This rev of the system will be using:

1. A sodium iodine detector, with high voltage power supply.
2. A capture and hold circuit on our custom Lux Interna board etched by Rab
3. A ADUC7061 24-bit analog-to-digital converter chip
   This chip comes to us on the Eval-ADUC7061MKZ eval board.
   We have seen it provide about 15 non-noisy bits out of the box
   but may be able to get more precision at a lower sampling rate.
4. A RaspberryPi (hawt!) to flow data from the ADC board's serial
   output to a file on the pi's disk (SD card), via custom software
   written in python

Data format
-----------

Under ideal conditions, the ADC would deliver 24 bits of data per event.
However, since we live in the real world, we predict that it maxes out
at about 18 bits of non-noisy data, though our data scheme provides for
up to 21 data bits per sample.

Each byte of output from the ADC board's serial port will reserve one
bit (the MSb) for control. This bit is on for the first byte (MSB) of
a sample, and off otherwise. The other 7 bits are data, and we always
expect 3 bytes per sample.

Usage
===========

pip install Pillow
python analyze/processData-ascii.py 13.rad
python analyze/analyzeBins-graph.py 13_bins.txt
