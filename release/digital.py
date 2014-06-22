from card import Card
import serial
import time
import string
import re

class Digital(Card):
    
    def __init__(self,id,serial):
        Card.__init__(self,id,serial)
        self.id = id
        self.__in_ports = ['0']*14
        self.__out_ports = ['0']*14
        self.__raw_out_ports = ''
        self.__raw_in_ports = ''
        self.__pending_write = 0

        
    def write_ports(self):
        if self.__pending_write :
            hex_data = self.__prepare_write()
            self.get_serial_channel().write(hex_data)
            time.sleep(self.get_response_latency())
            card_response = self.get_serial_channel().read(1)
            
        
    def read_ports(self):        
        self.get_serial_channel().write(self.id.decode('hex'))
        time.sleep(self.get_response_latency())
        card_response = self.get_serial_channel().read(2)
        card_address = self.get_serial_channel().read(1)                                                   
        self.__process_read(card_response)

    def set_ports(self,ports):
        for i in range(len(ports)):
            ports[i] = str(ports[i])
        self.__pending_write = 1 
        self.__out_ports = ports
            
        
    def __prepare_write(self):
        
        first_byte = self.__out_ports[0:7]
        last_byte = self.__out_ports[7:14]
        
        first_byte.append('0')
        last_byte.append('0')
        
        first_byte = string.join(first_byte,'')
        last_byte = string.join(last_byte,'')

        bin_id = self.hexToBin(self.id)
        bin_id = '1' + bin_id[1:len(bin_id)]
        
        write_id = ( '%02x' % int(bin_id,2) ).decode('hex')

        f =  '%02x' % int(first_byte,2) 
        l =  '%02x' % int(last_byte,2) 
        
        self.__raw_out_ports = f+l
        
        return write_id+self.__raw_out_ports.decode('hex')
    
    def __process_read(self,card_response):
        data = card_response.encode('hex')
        self.__raw_in_ports = data
        bin_data = self.hexToBin(data)
        for i in range(7):  
            self.__in_ports[i] = bin_data[i]
            self.__in_ports[ 7+i ] = bin_data[7+i]
    

    def __repr__(self):
        return "in: %s , out: %s" % (string.join(self.__in_ports,':'),string.join(self.__out_ports,':'))
        
    def need_flush(self):
        return self.__pending_write
    
    def __setattr__(self,name,value):
        port = re.match('^port_(\d+)', name) 
        if port  :
            port_pos = int((port.groups())[0])
            self.__pending_write = 1 
            self.__out_ports[port_pos] = str(value)
        else:
            Card.__setattr__(self,name,value)
            
    def __getattr__(self,name):
        port = re.match('^port_(in|out)_(\d+)', name) 
        if port :
            port_pos = int((port.groups())[1])
            type = (port.groups())[0]
            
            if type == 'in' :
                return int(self.__in_ports[port_pos])
            else:
                return int(self.__out_ports[port_pos])
        else:
            Card.__getattr__(self,name)
