#!/usr/bin/python

from channel.bus import Bus
from channel.digital import Digital
import yaml
b = Bus(0,False)
b.add_card(Digital(b.channel_id,0))
b.add_card(Digital(b.channel_id,2))        

b1 = Bus(1,True)
b1.add_card(Digital(b1.channel_id,0))
b1.add_card(Digital(b1.channel_id,0))        
b1.add_card(Digital(b1.channel_id,0))
b1.add_card(Digital(b1.channel_id,0))        



#print yaml.dump([b,b1])
print   "--------------"
yaml.dump(yaml.load(yaml.dump([b,b1])))
