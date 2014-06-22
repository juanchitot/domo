import yaml
from card import Card
from port import *
from card_exception import * 
import random
import serial
import time
import string
import re

class DebugCard(Card):
    
    def __init__(self,channel_id,card_number):
        Card.__init__(self,channel_id,card_number)
        for port_id in range(14):
            self.in_ports.append(InPort(channel_id,card_number,port_id,0))
            self.out_ports.append(OutPort(channel_id,card_number,port_id,0))
        self.simulation_mode = True
    
    def __str__(self):
        return "inP: %s , outP: %s" % ( string.join( [ '%s' % p.get_value() for p in self.in_ports ],','),
                                        string.join( [ '%s' % p.get_value() for p in self.out_ports ],',') )
    
    def card_mode(self):
        return 'rw'
    
    def read_card(self,raw_response=None):        
        pass
    
    def write_card(self,raw_response=None):        
        pass
    
    def reset_card(self,raw_response=None):
        pass
    
    def test_speed(self,response=None,mode='read'):
        if mode == 'write' :            
            return self.write_card(response) 
        else :
            return self.read_card(response) 

yaml.add_constructor(u'!DebugCard',DebugCard.yaml_constructor)
yaml.add_representer(DebugCard, DebugCard.yaml_representer)


    
