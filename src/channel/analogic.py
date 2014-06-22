import yaml
from card import Card
from port import InPort
from card_exception import * 
import time 
import re
import string
import random

class Analogic(Card):
    
    READ_RESPONSE_SIZE = 10
    RESET_RESPONSE_SIZE = 10
    
    def __init__(self,bus_id,card_number):
        Card.__init__(self,bus_id,card_number)
        for port_id in range(9):
            self.in_ports.append(InPort(bus_id,card_number,port_id,0))
        self.raw_in_ports = '00'*9
    
    def __ports_to_string(self):
        st = ''
        for i in range(9):
            st += '-'+str((self.in_ports[i]).get_value())
        return st

    def __str__(self):
        return "in: %s raw:%s" % (self.__ports_to_string(),self.raw_in_ports)
    
    def card_mode(self):
        return 'r'   
    
    def from_ports_to_raw(self,ports_type=None):
        new_raw_in_ports = ''
        for i in range(9) :
            new_raw_in_ports += '%02x' % self.in_ports[i].get_value()
        self.raw_in_ports = new_raw_in_ports
        
    def from_raw_to_ports(self,ports_type=None):
        for i in range(9) :
            old_value = self.in_ports[i].get_value()
            read_value = int(self.raw_in_ports[i*2:i*2+2],16)
            new_value = read_value
            #
            #if old_value+1 < read_value :
            #    new_value +=  1
            #elif old_value-1 > read_value:
            #    new_value -= 1               
            #
            self.in_ports[i].set_value(new_value)
        
    def generate_random_read_response(self):
        prob_by_throw = self.read_error_probability / 2
        r = random.random()
        r1 = random.random()
        
        if r < prob_by_throw :
            #error en la longitud de la respuesta
            # print " prob_by_throw es %f r es: %f y r1 es: %f " % (prob_by_throw,r,r1)        
            ret = '00000000'
        elif r1 < prob_by_throw :
            #error en el id de la respuesta
            # print " prob_by_throw es %f r es: %f y r1 es: %f " % (prob_by_throw,r,r1)        
            ret = "0000%02x" % (self.card_number+1)        
        else:
            #respuesta correcta
            ret = '%02x'*10 % (random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255),
                               self.card_number)
            #print "entro a la respuesta correcta %s" % ret
                        
        return ret.decode('hex')

    def read_card(self,raw_response=None):        
        if raw_response:        
            
            # genero una respuesta aleatoria si esta en modo simulacion
            if self.simulation_mode :
                raw_response = self.generate_random_read_response()
            
            if len(raw_response) <> 10 :
                e = CardResponseException("Error en la longitud de la respuesta, placa %s\
, se esperaban 20 bytes, (%d)" % (self.get_id(),len(raw_response)*2))
                e.operation = CardException.READ_OPERATION
                e.card_id = self.get_id()
                raise e
            
            raw_more_id = raw_response.encode('hex')
            
            if int(raw_more_id[18:20],16) <> ( self.card_number + 1 ) :
                e = CardResponseException("Error en la respuesta, la placa que respondio \
posee id %s y se esperaba %02x " % ( raw_more_id[18:20], self.card_number + 1 ))
                e.card_id = self.get_id()
                e.operation = CardException.READ_OPERATION
                raise e
            self.raw_in_ports = raw_more_id[0:18]
            self.from_raw_to_ports()
        else:
            return ('%02x' % (self.card_number + 1) ).decode('hex') 
    
    def test_speed(self,response=None,mode=None):
        return self.read_card(response)

    def write_card(self,raw_respose=None):
        pass
    
    def reset_card(self,raw_response=None):
        raw = '%02x' % (self.card_number+1)
        return raw.decode('hex')

yaml.add_constructor(u'!Analogic',Analogic.yaml_constructor)
yaml.add_representer(Analogic, Analogic.yaml_representer)

class TestAnalogic:
    
    def run(self):
        a = Analogic('Bus_0',40)
        print "printeo el card read"
        print a.read_card().encode('hex')
        
        a.read_card('01020304050607081029'.decode('hex'))
        print a


if __name__ == '__main__' :
    test = TestAnalogic()
    test.run()
