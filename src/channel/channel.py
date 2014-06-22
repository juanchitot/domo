import logger.domotica_logger
import logging
import time
import sys
from threading import Thread, Event
from channel_exception import ChannelException
from configurator.domotica_serialize import DomoticaSerialize

class Channel(Thread,DomoticaSerialize):
    
    logger_instance = logging.getLogger('domotica.channel')
    channels = {}
    current_channel = None
    channels_order = []
    
    def __init__(self,id):
        Thread.__init__(self)        
        
        self.channel_id = '%s_%d' % (self.__class__.__name__, id)
        self.name = self.channel_id
        self.event = Event()
        self.run_until = -1 #run forever
        self.paused = False
    
    def get_id(self):
        return self.channel_id
    
    def get_in_ports(self):
        return self.in_ports
    
    def get_out_ports(self):
        return self.out_ports
    
    def work(self):
        pass
    
    def run(self):
        
        while self.run_until :            
            if self.run_until > 0 : 
                self.run_until -= 1            
            if not self.paused :
                self.work()
    
    def stop(self):
        self.run_until = False
    
    def reset(self):
        pass
    
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def __repr__(self):
        ins = ''
        
        k =  self.in_ports.keys()
        k.sort()
        for p_i in k:
            ins += '(%s,%d)' % (p_i,id(self.in_ports[p_i]))
            
        k =  self.out_ports.keys()
        k.sort()
        outs = ''        
        for p_i in k:
            outs += '(%s,%d)' % (p_i,id(self.out_ports[p_i]))
            
        return ins + "\n" + outs
        
            
            
