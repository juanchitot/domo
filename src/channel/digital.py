import yaml
from card import Card
from port import *
from card_exception import * 
import random
import serial
import time
import string
import re

class Digital(Card):
    
    def __init__(self,channel_id,card_number):
        Card.__init__(self,channel_id,card_number)
        for port_id in range(14):
            self.in_ports.append(InPort(channel_id,card_number,port_id,0))
            self.out_ports.append(OutPort(channel_id,card_number,port_id,0))
        self.raw_out_ports = '00'
        self.raw_in_ports = '00'
    
    def __ports_to_bin(self,inOut):
        bin_data=''
        if inOut == 'in' :
            ports = self.in_ports
        else:
            ports = self.out_ports
        for port_id in range(len(ports)):
            bin_data += str(ports[port_id].get_value())
        return bin_data 
    
    def __str__(self):
        return "inP: %s , outP: %s, inR: %s, outR: %s " % (self.__ports_to_bin('in'),
                                                           self.__ports_to_bin('out'),
                                                           self.raw_in_ports,
                                                           self.raw_out_ports)
    
    def card_mode(self):
        return 'rw'

    def from_raw_to_ports(self,ports='in'):
        if ports == 'in' :
#             print "hago la conversion de raw a ports en read"
#             print self.raw_in_ports
            bin_data = Card.hex_to_bin(self.raw_in_ports)
            # los dos ultimos bits de los 2 bytes no sirven            
            Card.logger_instance.debug("from_raw_to_ports in: bin_data %s %s %s %s  hex_data %s" % (bin_data[0:4],bin_data[4:8],bin_data[8:12],bin_data[12:16],self.raw_in_ports))
            bin_data = bin_data[0:7] + bin_data[8:15]
            for port_id in range(len(self.in_ports)):
                self.in_ports[port_id].set_value(int(bin_data[port_id]))
        else:
            bin_data = Card.hex_to_bin(self.raw_out_ports)
            for port_id in range(len(self.out_ports)):
                self.out_ports[port_id].set_value(int(bin_data[port_id]))
    
    def from_ports_to_raw(self,ports='out'):
        if ports == 'out' :
            bin_data=''
            for port_id in range(len(self.out_ports)):
                if port_id == 7:
                    bin_data += '0'
                bin_data += str(self.out_ports[port_id].get_value())
            bin_data += '0'
            self.raw_out_ports = '%02x' % int(bin_data[8:16],2)
            self.raw_out_ports += '%02x' % int(bin_data[0:8],2)
            Card.logger_instance.debug("from_ports_to_raw out: bin_data %s %s %s %s  hex_data %s" % (bin_data[0:4],bin_data[4:8],bin_data[8:12],bin_data[12:16],self.raw_out_ports))
        else:
            bin_data=''
            for port_id in range(len(self.in_ports)):
                if port_id == 7:
                    bin_data += '0'
                bin_data += str(self.in_ports[port_id].get_value())
            bin_data += '0'
            self.raw_in_ports = '%02x' % int(bin_data[8:16],2)
            self.raw_in_ports += '%02x' % int(bin_data[0:8],2)

            
    def generate_random_read_response(self):
        prob_by_throw = self.read_error_probability / 2
        if random.random() < prob_by_throw :
            #error en la longitud de la respuesta
            ret = '000000'
        elif random.random() < prob_by_throw :
            #error en el id de la respuesta
            ret = "0000%02x" % (self.card_number)        
        else:
            #respuesta correcta
            ret = '%02x%02x%02x' % (random.randint(0,255),
                                    random.randint(0,255),
                                    self.card_number+1)
        return ret.decode('hex')

    def generate_random_write_response(self):
        if random.random() < self.write_error_probability :
            #error en el id de la respuesta
            ret = "%02x" % (self.card_number+1)        
        else:
            #respuesta correcta
            ret = '%02x' % (self.card_number + 129)
        return ret.decode('hex')

#
# Leo los valores de entrada de la targeta 
# Primero se usa esta funcion para enviar el pedido de lectura
# a la targeta. Y despues para procesar la respuesta
#
    def read_card(self,raw_response=None):        
        if raw_response:        
            # genero una respuesta aleatoria si esta en modo simulacion
            if self.simulation_mode :
                raw_response = self.generate_random_read_response()

            if len(raw_response) <> self.READ_RESPONSE_SIZE :
                e = CardResponseException("Error en la longitud de la respuesta, placa %s\
, se esperaban 6 bytes, (%d) %s" % (self.get_id(),len(raw_response), raw_response.encode('hex') ))
                e.operation = CardException.READ_OPERATION
                e.card_id = self.get_id()
                raise e
            
            raw_more_id = raw_response.encode('hex')
            
            if int(raw_more_id[4:6],16) <> (self.card_number + 1) :
                e = CardResponseException("Error en la respuesta, se esperaba la respuesta de la placa %s (%02x) y se recibio %s" % (self.get_id(), (self.card_number+1), raw_more_id[4:6]))
                e.card_id = self.get_id                
                e.operation = CardException.READ_OPERATION
                raise e
            self.raw_in_ports = raw_more_id[0:4]
            self.from_raw_to_ports()
            Card.logger_instance.debug("en read_card digital %02x respondio %s" % (self.card_number + 1,self.raw_in_ports))
        else:
            Card.logger_instance.debug("en read_card digital %02x" % (self.card_number + 1))
            return ('%02x' % (self.card_number + 1) ).decode('hex') 
    
    def write_card(self,raw_response=None):        
        if raw_response:        
            if self.simulation_mode :
                raw_response = self.generate_random_write_response()                
                
            if len(raw_response) <> self.WRITE_RESPONSE_SIZE :
                e = CardResponseException("Error en la longitud de la respuesta, placa %s\
, se esperaban 6 bytes, (%d) %s" % (self.get_id(),len(raw_response), raw_response.encode('hex') ))
                e.operation = CardException.WRITE_OPERATION
                e.card_id = self.get_id()
                raise e
            
            raw_encoded = raw_response.encode('hex')
            if raw_encoded <> '%02x' % (self.card_number + 129) :
                e = CardResponseException("Error en la respuesta, se esperaba la respuesta de la placa %s (%02x) y se recibio %s" % (self.get_id(), (self.card_number+129), raw_encoded))
                e.card_id = self.get_id                
                e.operation = CardException.WRITE_OPERATION
                raise e           
            Card.logger_instance.debug("en write_card digital %02x escribio  %s" % (self.card_number + 1,self.raw_out_ports))
        else:
            self.from_ports_to_raw()
            raw_encoded = '%02x' % ( self.card_number + 129 ) 
            raw_encoded += self.raw_out_ports
            Card.logger_instance.debug("en write_card digital  contenido de raw_out_ports %s" % (self.raw_out_ports))
            Card.logger_instance.debug("en write_card digital escribio  %s" % ( raw_encoded))
            return raw_encoded.decode('hex')
            
            
    def reset_card(self,raw_response=None):
        raw_encoded = '%02x' % ( self.card_number + 129 )
        raw_encoded += '0000'
        #mando "id0000id0000" en hexa para resetear el channel
        raw_encoded *= 2 
        return raw_encoded.decode('hex')
        
#
# Operacion de prueba que se utiliza para 
# testear la velocidad de la placa
#
    def test_speed(self,response=None,mode='read'):
        if mode == 'write' :            
            return self.write_card(response) 
        else :
            return self.read_card(response) 

yaml.add_constructor(u'!Digital',Digital.yaml_constructor)
yaml.add_representer(Digital, Digital.yaml_representer)
