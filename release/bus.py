import serial
from analogic import Analogic
from digital import Digital


class Bus:
    def __init__(self,id):
        self.__id = id
        self.__cards = {}
        self.__serial = serial.Serial(id)
    
    def add_card(self,card_id,card_type):
        if card_type == 'Digital' :
            self.__cards[card_id] = Digital(card_id,self.__serial)
        elif card_type == 'Analogic' :
            self.__cards[card_id] = Analogic(card_id,self.__serial)
        
    def read_cards(self):
        for (id,card) in self.__cards.iteritems():
            card.read_ports()
            print card
    
    def get_card(self, id):
        return self.__cards[id]
    
    def flush_cards(self):
        print "hago un flush cards"
        for (id,card) in self.__cards.iteritems():
            print "en el for"
            if card.need_flush() : 
                print "need flush"
                card.write_ports()
                print card
    
