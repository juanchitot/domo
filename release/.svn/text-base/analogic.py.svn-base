from card import Card
import time 
import re
import string

class Analogic(Card):
    
    def __init__(self,id,serial):
        Card.__init__(self,id,serial)
        self.id = id
        self.__in_ports = [0]*9
        self.__raw_data = ''

        
        
    def read_ports(self):        
        self.get_serial_channel().write(self.id.decode('hex'))
        time.sleep(self.get_response_latency())
        card_response = self.get_serial_channel().read(9)
        card_address = self.get_serial_channel().read(1)                                                   
        self.__process_read(card_response)

    
    
    def __process_read(self,card_response):
        data = card_response.encode('hex')       
        self.__raw_data = data
        for i in range(9) :  
            self.__in_ports[i] = int(data[i*2:(i*2)+2],16)
    

    def __repr__(self):
        return "in: %s raw:%s" % (str(self.__in_ports),self.__raw_data)

    def __getattr__(self,name):
        port = re.match('^port_in_(\d+)', name) 
        if port :
            port_pos = int((port.groups())[0])      
            return self.__in_ports[port_pos]
        else:
            Card.__getattr__(self,name)
        

