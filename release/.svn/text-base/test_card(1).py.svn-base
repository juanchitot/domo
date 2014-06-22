#!/usr/bin/python

from card.bus import Bus
import time

b = Bus(0)
b.add_card('00','Digital')
#b.add_card('16','Analogic')
b.read_cards()

c=b.get_card('00')
c.set_ports([0,0,0,0,0,0,0]*2)

for i in range(14):    
    c.__setattr__('port_%d' % i, 1)
    b.flush_cards()
    time.sleep(1)
    c.__setattr__('port_%d' % i, 0)
    b.flush_cards()
    
b.read_cards()
