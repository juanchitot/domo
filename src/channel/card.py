import logger.domotica_logger
import logging
import re
import yaml
import inspect
from port import InPort,OutPort 
from card_exception import CardException

from configurator.domotica_serialize import DomoticaSerialize

class Card(DomoticaSerialize):
    
    HEX_TO_BIN_TABLE = {'0' : '0000',
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

    READ_ERROR_PROBABILITY = 0.0001
    WRITE_ERROR_PROBABILITY = 0.01 
    
    READ_RESPONSE_SIZE = 3
    WRITE_RESPONSE_SIZE = 1
    RESET_RESPONSE_SIZE = 0
    
    RESET_WAIT_TIME = 0.2
    
    logger_instance = logging.getLogger('domotica.channel.card')

    constructor_params = ['channel_id','card_number']
    
    def __init__(self,channel_id,card_number):        
        self.card_number = int(card_number)
        self.channel_id = channel_id
        self.card_id = "%s_%02d" % (channel_id,card_number)
        self.in_ports = []
        self.out_ports = []
        self.set_default_probabilitys()
        self.simulation_mode = False
        self.timeout_cote = 0
    
    # Se encarga de mantener sincronizado el estado 
    # interno del objeto(en hexa) con el valor
    # de los puertos que exporta.
    # Escribe el actualiza el valor de interno del objeto(Hexa)
    # con el valor de los puertos que "exporta" (inports)
        
    def from_ports_to_raw(self,ports_type='out'):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))

    # Actualiza el valor de los ports con el valor 
    # interno del objeto(outports)
    
    def from_raw_to_ports(self,ports_type='in'):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))
    
    def get_id(self): 
        return self.card_id 
    
    
    # In Ports exportados por esta targeta
    
    def get_in_ports(self):
        return self.in_ports
    
    
    # Out Ports exportados por esta targeta

    def get_out_ports(self):
        return self.out_ports
    
    
    # Funcion para convertir strings de Hexa en Strings
    # binarios

    def hex_to_bin(hex_data):
        bin_data = ''
        for hex_chr in hex_data.upper() :
            bin_data += Card.HEX_TO_BIN_TABLE[hex_chr]        
        return bin_data 
    hex_to_bin = staticmethod(hex_to_bin)
    
    
    # Metodo a travez del cual el bus habla con la placa, primero
    # para mandar el pedido de lectura y una vez recibidos los 
    # datos por el bus, para hacer el procesamiento y actualizar 
    # el estado interno de la placa

    def read_card(self,raw_response=None):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))
    
#     def read_test(self,raw_response=None):
#         raise NotImplementedError("Metodo %s no implementado en la clase %s" %
#                                   (inspect.stack()[0][3],
#                                    self.type()))
    
    def set_default_probabilitys(self):
        self.read_error_probability = self.READ_ERROR_PROBABILITY
        self.write_error_probability = self.WRITE_ERROR_PROBABILITY
            
    def set_probabilitys(self, probabilitys):
        if 'read_error_probability' in probabilitys :            
            self.read_error_probability = probabilitys['read_error_probability']
        
        if 'write_error_probability' in probabilitys :            
            self.write_error_probability = probabilitys['write_error_probability']
    
    
    def set_simulation_mode(self,probabilitys={}):
        self.simulation_mode = True
        self.set_probabilitys(probabilitys)
    
    
    def type(self):
        return self.__class__.__name__
    
    def card_mode(self):
        return ''
    
    def test_speed(self,response=None):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))
    
    def unset_simulation_mode(self):
        self.simulation_mode = False

    
    def write_card(self,raw_response=None):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))
        
    def write_test(self,raw_response=None):
        raise NotImplementedError("Metodo %s no implementado en la clase %s" %
                                  (inspect.stack()[0][3],
                                   self.type()))
    def __repr__(self):
        return '%s: %s, %d' % ( self.__class__.__name__, self.channel_id, self.card_number)
    
        
                              
