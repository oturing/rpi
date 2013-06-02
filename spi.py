#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import atexit
import RPi.GPIO as GPIO

# assegurar que a função cleanup será chamada na saída do script
atexit.register(GPIO.cleanup)

# usar numeração lógica dos pinos
GPIO.setmode(GPIO.BCM)

# definir pinos que serão usados para implementar SPI
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# configurar pinos
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# ler dados do MCP3008 usando protocolo SPI
def ler_canal(canal):
    assert 0 <= canal <= 7, 'canal deve ser de 0 a 7'
    GPIO.output(SPICS, True)    
    GPIO.output(SPICLK, False)
    GPIO.output(SPICS, False)
    cmd = canal
    cmd |= 0x18  # bit inicial + bit configuração "single-ended"
    cmd <<= 3    # descartar 3 bits; usaremos apenas 5
    for i in range(5):
        GPIO.output(SPIMOSI, cmd & 0x80)
        cmd <<= 1
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)

    res = 0
    # ler bit nulo e 10 bits do valor ADC
    for i in range(11):
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)
        res <<= 1
        if (GPIO.input(SPIMISO)):
            res |= 0x1

    GPIO.output(SPICS, True)
    return res

#import pdb; pdb.set_trace()
contador = 0
display = '{0:6d}  {1:010b}  {1:4}  {2:3.2f} V {3}'
while True:
    res = ler_canal(1)
    volts = float(res)/1023 * 3.3
    marcas = int(round(float(res)/1023*40))*'='
    print display.format(contador, res, volts, marcas)
    time.sleep(.2)
    contador += 1
    
