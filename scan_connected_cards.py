#!/usr/bin/python

import time
from serial import Serial

serial_port = Serial(0)

if not serial_port.isOpen(): 
    print "No se pudo habrir el puerto serial /dev/ttyS0 "

serial_port.flushInput()
serial_port.flushOutput()

id = 0
while id < 128 :
    print "pruevo %d" % id
    query_str = ('%02x' % id ).decode('hex') 
    serial_port.write(query_str)
    time.sleep(0.9)
    waiting = serial_port.inWaiting()
    if waiting :
        print "La placa con id %d %02x respondio" % (id,id)
        serial_port.read(waiting)
    id += 1
