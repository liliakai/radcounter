Yet another iteration of our home-made radiation spectrometer.

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
