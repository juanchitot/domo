import random
import time
import re
import yaml
import serial
import sys

from serial import Serial

from core.domotica_exception import DomoticaException
from card_exception import CardException
from card_exception import CardResponseException
from card_exception import CardTimeoutException
from card import Card
from analogic import Analogic
from digital import Digital
from port import InPort,OutPort
from channel import Channel
from bus_exception import BusException




# TODO:
# - Posibilitar desabilitar temporariamente una targeta


class Bus(Channel):
    
    
    supported_card_types = ['Digital','Analogic','DebugCard']
    
    #(50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 
    #2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 
    #460800, 500000, 576000, 921600, 1000000, 1152000, 
    #1500000, 2000000, 2500000, 3000000, 3500000, 4000000)
    
    baud_rate = 1152000
    TIMEOUT_PROBABILITY = 0.0001
    CARD_ERROR_PROBABILITY = 0.0001
    
    constructor_params = ['bus_number','simulation_mode']
    serializable_data = {'cards':'cards'}
    
    def __init__(self,bus_number,simulation_mode=False):
        Channel.__init__(self,bus_number)
        
        self.bus_number = bus_number
        self.bus_id = bus_number
        self.cards = {}
        self.in_ports = {}
        self.out_ports = {}        
        
        self.serial = serial.Serial()
        self.serial.port = self.bus_id
        self.serial.baudrate = Bus.baud_rate
        self.simulation_mode = False
        
        if simulation_mode : 
            self.start_simulation_mode()
        else :
            self.connect()     
        
        self.set_default_probabilitys()        
    
    
    def connect(self):        
        if not self.simulation_mode :
            try :
                self.serial.open()
            except SerialException, e :
                b_e = BusException(e)
                b_e.log(self.logger_instance)
                raise b_e
            except Exception, e:
                b_e = BusException(e)
                b_e.log(self.logger_instance)
                raise b_e
            
            if not self.serial.isOpen() :
                raise BusException("No se pudo abrir el Serial %d " % self.bus_id)
            else: 
                pass
    
    def connected(self):
        return self.serial.isOpen()
    
    def add_card(self,card):
        """
        Conecta una tarjeta a un bus
        :param card:
        :return: cardId :raise BusException:
        """
        if not isinstance(card,Card) :
            raise BusException("El tipo de targeta %s no es soportado por este bus" % 
                               card.__class__.__name__)
        
        self.cards[card.card_number] = card
        for port in card.get_in_ports():
            self.in_ports[port.get_id()] = port
        for port in card.get_out_ports():
            self.out_ports[port.get_id()] = port
        return card.get_id()
    
    def remove_card(self,card_id):
        if card_id in self.cards:
            m = re.compile('%s_I_%02d_\d{2}' % (self.channel_id,card_id))
            for p_k, p in  self.in_ports.items():
                if m.match(p_k):
                    del self.in_ports[p_k]
            
            m = re.compile('%s_O_%02d_\d{2}' % (self.channel_id,card_id))
            for p_k, p in self.out_ports.items():
                if m.match(p_k):
                    del self.out_ports[p_k]
            
            del self.cards[card_id]
                
    
    def get_card(self,card_number_or_id):
        match = re.match('^([a-z]+)_(\d+)$',card_number_or_id,re.I) 
        if match :
            card_number = match.group(2)
        elif isinstance(card_number_or_id, int) :
            card_number = card_number_or_id
        else :
            raise BusException("El numero o id de la targeta es incorrecto (%s)" % 
                               card_number_or_id)
        
        if card_number in self.cards :
            return self.cards[card_number]
        
        raise BusException("La placa numero %d no existe" % card_number)
            
    def read_card(self,card):        
        to_send = card.read_card()
        if card.simulation_mode or self.simulation_mode :
            r = random.random()
            if r < self.timeout_probability :
                e = CardTimeoutException( "Se produjo un timeout al leer la targeta %s random(%f<%f)" % (card.get_id(),r,self.timeout_probability) ) 
                e.operation = CardException.READ_OPERATION
                e.card_id = card.get_id()
                raise e
            read_response = True
        else:
            self.write(to_send)
#             cicles = 0
#             while self.serial.inWaiting() <> card.READ_RESPONSE_SIZE and cicles < card.timeout_cote :                
#                 cicles += 1
            
            send_time = time.time()
            while (time.time() - send_time) < 2 and self.serial.inWaiting() <> card.READ_RESPONSE_SIZE :
                pass
            
            inWaiting = self.serial.inWaiting()
            read_response = self.read(inWaiting)

            if inWaiting <> card.READ_RESPONSE_SIZE :
                e = CardTimeoutException( "Se produjo un timeout al leer la targeta %s, response ( %s ) " % ( card.get_id(), read_response.encode('hex') ) )                            
                e.operation = CardException.READ_OPERATION
                e.card_id = card.get_id()
                raise e
            
        card.read_card(read_response)

        
    def read_cards(self):
        cards_numbers = self.cards.keys()
        for card_number in cards_numbers :
            
            card = self.cards[card_number]            
            
            if not 'r' in card.card_mode() :
                continue
            try : 
                self.read_card(card)
            except DomoticaException, e :
                e.log(self.logger_instance)                
            except Exception, e:
                d_e = DomoticaException("Excepcion no esperada en read card\
 con card_id = %s (%s) "(card.get_id(),e))
                d_e.log(self.logger_instance)
    
    def write_card(self,card):        
        to_send = card.write_card()
        if card.simulation_mode or self.simulation_mode :
            r = random.random()
            if r < self.timeout_probability :
                e = CardTimeoutException( "Se produjo un timeout al escribir la targeta %s random(%f<%f)" % (card.get_id(),r,self.timeout_probability) ) 
                e.operation = CardException.WRITE_OPERATION
                e.card_id = card.get_id()
                raise e
            write_response = True
        else:
            self.write(to_send)
#             cicles = 0
#             while self.serial.inWaiting() <> card.WRITE_RESPONSE_SIZE and cicles < card.timeout_cote :
#                 cicles += 1
            
            send_time = time.time()
            while (time.time() - send_time) < 2 and self.serial.inWaiting() <> card.WRITE_RESPONSE_SIZE :
                pass
            
            inWaiting = self.serial.inWaiting()
            write_response = self.read(inWaiting)
            
            if inWaiting <> card.WRITE_RESPONSE_SIZE :
                e = CardTimeoutException( "Se produjo un timeout al escribir la targeta %s,\
 response ( %s ) " % ( card.get_id(), write_response.encode('hex') ) ) 
                e.operation = CardException.WRITE_OPERATION
                e.card_id = card.get_id()
                raise e
        
        card.write_card(write_response)
    
    def write_cards(self):
        cards_numbers = self.cards.keys()
        for card_number in cards_numbers :
            
            card = self.cards[card_number]            
            
            if not 'w' in card.card_mode() :
                continue
            try : 
                self.write_card(card)
            except DomoticaException, e :
                e.log(self.logger_instance)                
            except  Exception, e: 
                d_e = DomoticaException("Excepcion no esperada en write card\
 con card_id = %s (%s) "(card.get_id(),e.message))
                d_e.log(self.logger_instance)                
        
    
    def set_default_probabilitys(self):
        self.timeout_probability = self.TIMEOUT_PROBABILITY
        self.card_error_probability = self.CARD_ERROR_PROBABILITY
        
        for card in self.cards:
            card.set_default_probabilitys()
    
    
    def set_probabilitys(self, probabilitys={}):
        if 'timeout_probability' in probabilitys :            
            self.timeout_probability = probabilitys['timeout_probability']
        
        if 'card_error_probability' in probabilitys :            
            self.card_error_probability = probabilitys['card_error_probability']
        
        for card in self.cards:
            card.set_probabilitys(probabilitys)
    
            
    def start_simulation_mode(self, probabilitys={}):
        self.simulation_mode = True
        self.set_probabilitys(probabilitys)
        for card in self.cards:
            card.set_simulation_mode()        
        
    def stop_simulation_mode(self):
        self.simulation_mode = false
        if not self.connected() :
            self.connect()
            
    def test_cards_speeds(self,card_id=None):
        if card_id :
            cards_numbers = [card_id]
        else:
            self.reset()
            cards_numbers = self.cards.keys()
#         print "card_id "
#         print cards_numbers
        for c_id in cards_numbers :
            for i in range(5):
                if 'r' in  self.cards[c_id].card_mode():
                    try :
                        self.test_card_speed(c_id,'read')
                    except DomoticaException, e:
                        e.log(self.logger_instance)
                    except Exception, e:
                        d_e = DomoticaException(e)
                        d_e.log(self.logger_instance)
                    else:
                        self.logger_instance.info("Test %d card %s OK" %(i,c_id))
                if 'w' in self.cards[c_id].card_mode():
                    try : 
                        self.test_card_speed(c_id,'write')
                    except DomoticaException, e:
                        e.log(self.logger_instance)
                    except Exception,e:
                        d_e = DomoticaException(e)
                        d_e.log(self.logger_instance)
                
                self.logger_instance.debug("La placa %s tiene timeout_cote = %d " % (c_id, self.cards[c_id].timeout_cote))                

    
            
    def reset_card(self,card):
        if not card.simulation_mode :
            to_reset = card.reset_card()            
            
            if card.RESET_RESPONSE_SIZE :
                cicles = 0
                self.write(to_reset)            
                
                time_before = time.time()                        
                
                while self.serial.inWaiting() <> card.RESET_RESPONSE_SIZE and (time.time() - time_before) < 3 :
                    cicles += 1 
                
                if self.serial.inWaiting() <> card.RESET_RESPONSE_SIZE :
                    e = CardTimeoutException( "Se produjo un timeout al resetear la targeta %s cicles %d" % (card.get_id(),cicles) ) 
                    e.operation = CardException.RESET_OPERATION #completar
                    e.card_id = card.get_id()
                    raise e
                else:
                    response = self.read(self.serial.inWaiting())
                    card.reset_card(response)
            else:
                self.logger_instance.debug("La placa %s tiene excribe %s para el reset" % (card.card_id, to_reset.encode('hex')))                
                self.write(to_reset)
                time.sleep(card.RESET_WAIT_TIME)
                self.read(self.serial.inWaiting())                
    
    def test_card_speed(self, card_id, mode='read'):
        
        self.logger_instance.debug("entro en test_card_speed con card_id %s" % card_id )
        card = self.cards[card_id]
        
        self.reset_card(card)
        
        to_send = card.test_speed(None,mode)

        if not card.simulation_mode :
            
            self.logger_instance.debug("en test_card_speed escribo %s " % to_send.encode('hex'))
            self.reset()
            
            cicles = 0
            time_before = time.time()                        
            self.write(to_send)
            card_response_size = card.READ_RESPONSE_SIZE if mode == 'read' else card.WRITE_RESPONSE_SIZE 
            
            #pongo como maximo tiempo de respuesta para el test 2 segundos
            while self.serial.inWaiting() <> card_response_size and (time.time() - time_before) < 2 :
                cicles += 1 
            
            if self.serial.inWaiting() <> card_response_size :
                e = CardTimeoutException( "Se produjo un timeout al testear la targeta %s, mode = %s cicles %d" % (card.get_id(),mode,cicles) ) 
                e.card_id = card.get_id()
                raise e
            else:
                response = self.read(self.serial.inWaiting())
                try :
                    card.test_speed(response,mode)
                except DomoticaException, e:
                    e.message = "Se recibieron datos incorrectos durante un\
 test_card_speed de la placa %d, mode = %s, (%s)" % ( card.get_id(),mode,e.message)
                    raise e
                except Exception, e:
                    d_e = DomoticaException("Se produjo un error durante el test card\
 speed de la placa %d, mode = %s,(%s)" % ( card.get_id(),mode,e.message))
                    raise d_e
                
                new_cote = cicles + int(cicles * 0.30) 
                if not card.timeout_cote or card.timeout_cote < new_cote: 
                    card.timeout_cote = new_cote
                self.logger_instance.debug("La placa %s tiene timeout_cote = %d " % (card_id, card.timeout_cote))                
        else:
            
            if random.random() < self.timeout_probability :
                e = CardTimeoutException( "Se produjo un timeout al testear la targeta %s " % card.get_id() ) 
                e.operation = CardException.TEST_OPERATION
                e.card_id = card.get_id()
                raise e            
            count = random.randint(2500,3700)
            
            if card.timeout_cote < count :                
                card.timeout_cote = count
    
    def work(self):
        self.read_cards()
        self.write_cards()
        
    def reset(self):
        self.serial.flushOutput()
        self.serial.flushInput()
        
    def write(self,data,reset=True):
        if reset :
            self.reset()        
        self.logger_instance.debug("Bus I/O,  escribe : (%s)" % data.encode('hex') )                
        self.serial.write(data)
        
    def read(self,size=1):        
        response = self.serial.read(size)
        self.logger_instance.debug("Bus I/O,  lee : (%s)" % response.encode('hex'))                
        return response
        
#     Dump
#     - se guardan los parametros del constructor Bus(bus_id,simulation_mode)
#     - luego se guarda el array de targetas conectadas al bus
#     que esta en self.cards
#     @classmethod
#     def yaml_representer(cls,dumper,data):       
#         rpr = {'bus_id' : data.bus_id,
#                'simulation_mode' : data.simulation_mode,
#                'cards' : data.cards }
#         return dumper.represent_mapping(u'!Bus', rpr)

#     Load
#     - levanto algo de la forma "Bus: (\d), (True|False)" que utilizo
#     como parametros para el constructor    
    @classmethod    
    def yaml_constructor(cls,loader,node):        
        [constructor_params,data_items] = loader.construct_sequence(node,True)
        bus = Bus(*constructor_params)
        for k,v in data_items.items():
            if k == 'cards':
                for id,card in v.items():
                    bus.add_card(card)
            else:
                setattr(bus,k,v)
        return bus
    
    @classmethod    
    def search_connected_cards(cls,channel_number):
        try :
            print channel_number
            serial_port = Serial(int(channel_number))
        except Exception, e:
            d_e = DomoticaException(e)
            d_e.log(cls.logger_instance)
            return  "No se pudo habrir el puerto serial %s" % serial_port.port

        if not serial_port.isOpen(): 
            return  "No se pudo habrir el puerto serial %s" % serial_port.port

        serial_port.flushInput()
        serial_port.flushOutput()
            
        id = 0
        cards = ""
        while id < 128 :
            query_str = ('%02x' % id ).decode('hex') 
            serial_port.write(query_str)
            time.sleep(0.7)
            waiting = serial_port.inWaiting()
            if waiting :
                cards +=  "La placa con id %d hex(%02x) respondio\n" % (id,id)
                serial_port.read(waiting)
            id += 1
        serial_port.close()
        return cards
                

    
yaml.add_constructor(u'!Bus',Bus.yaml_constructor)
yaml.add_representer(Bus, Bus.yaml_representer)
    
            

class TestBus:
    
        
    def test(self):
        bus_0 = Bus(0,False)
#         bus_2 = Bus(2,True)        
        
#         bus_0.set_probabilitys({'timeout_probability':0.001,
#                                 'card_error_probability': 0.001 })
        
        bus_0.add_card(Digital(bus_0.channel_id,2))
                
        bus_0.test_cards_speeds()
        
        out_ports = bus_0.get_out_ports()
        
        bus_0.start()
        
#         keys = out_ports.keys()
#         keys.sort()
#         for port_id in keys:
#             port = out_ports[port_id]
#             port.value = 1
#             print "prendo el port %s " % port_id
#             time.sleep(0.5) 
#             port.value = 0
#             time.sleep(0.5)
        raw_input("Presiones una tecla para termiar el programa")

        bus_0.stop()
        bus_0.join()
        
    def test_dump_load(self):
        bus_0 = Bus(0,False)
        bus_0.add_card(Digital(bus_0.channel_id,2))
        bus_0.add_card(Digital(bus_0.channel_id,6))
        bus_0.add_card(Digital(bus_0.channel_id,4))
        bus_2 = Bus(2,True)        
        bus_2.add_card(Digital(bus_2.channel_id,2))
        bus_2.add_card(Digital(bus_2.channel_id,4))
        print "dumpeo el bus_0 "
        print yaml.dump(bus_0)
        print "dump del bus_2"
        print yaml.dump(bus_2)
        print "load del dump del bus_2"
        d = yaml.dump(bus_2)
        print d
        bus=yaml.load(d)
        print "print de bus.channel_id %s y bus.channel.simulation_mode %s " % (bus.channel_id,bus.simulation_mode)        
        print "print de bus.cards"
        print bus.cards
        
    
    def run(self):
        self.test()
        #self.test_dump_load()



if __name__ == '__main__' :
    test = TestBus()
    test.run()
