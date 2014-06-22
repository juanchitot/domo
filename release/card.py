import re

class Card:
    
    __VALID_CARD_ID = '^\d\d$' 
    __RESPONSE_LATENCY = 0.1
    __HEX_TO_BIN_TABLE = {'0' : '0000',
                          '1' : '0001',
                          '2' : '0010',
                          '3' : '0011',
                          '4' : '0100',
                          '5' : '0101',
                          '6' : '0110',
                          '7' : '0111',
                          '8' : '1000',
                          '9' : '1001',
                          'A' : '1010',
                          'B' : '1011',
                          'C' : '1100',
                          'D' : '1101',
                          'E' : '1110',
                          'F' : '1111'}
    
    def __init__(self,id,serial):        
        self.__id = id
        self.__serial_channel = serial
    
    def __setattr__(self,name,value):
        if name == '__id' :
            if re.match(self.__VALID_CARD_ID, value) :
                self.__dict__[name] = value
            else :
                raise TypeError, 'Valor %s invalido para attributo id'
        else :
            self.__dict__[name] = value

            
    def get_id(self):
        return self.__id
    
    def get_serial_channel(self):
        return self.__serial_channel
    
    def get_response_latency(self):
        return self.__RESPONSE_LATENCY
    
    def hexToBin(self,hex_data):
        bin_data = ''
        for hex_chr in hex_data.upper() :
            bin_data += self.__HEX_TO_BIN_TABLE[hex_chr]
        
        return bin_data 
    
    def need_flush(self):
        return 0
