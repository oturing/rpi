#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import atexit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# assegurar que a função cleanup será chamada na saída do script
atexit.register(GPIO.cleanup)

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# ler dados do MCP3008 usando protocolo SPI
def ler_canal(canal):
        assert 0 <= canal <= 7, 'canal deve ser de 0 a 7'
        GPIO.output(SPICS, True)
        GPIO.output(SPICLK, False)  # start clock low
        GPIO.output(SPICS, False)   # bring CS low
        print canal
        cmd = canal
        print '{0:08b}'.format(cmd)
        cmd |= 0x18  # start bit + single-ended bit
        print '{0:08b}'.format(cmd)
        cmd <<= 3    # we only need to send 5 bits here
        print '{0:08b}'.format(cmd)
        for i in range(5):
                GPIO.output(SPIMOSI, cmd & 0x80)
                cmd <<= 1
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)

        res = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
                res <<= 1
                if (GPIO.input(SPIMISO)):
                        res |= 0x1

        GPIO.output(SPICS, True)
        print '{0:012b}'.format(res)
        res >>= 1       # first bit is 'null' so drop it
        return res

import pdb; pdb.set_trace()
print 'lido:', ler_canal(3)


