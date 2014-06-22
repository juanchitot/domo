#!/usr/bin/python

from card.bus import Bus
import time

b = Bus(0, True)
b.set_probabilitys({'timeout_probability':0.01,
                    'card_error_probability': 0.01 })

# 'read_error_probability': self.read_error_probability ,
#                                       'write_error_probability': self.write_error_probability
b.add_card(0,'Digital')
b.add_card(1,'Analogic')
b.read_cards()
b.test_cards_speeds()
print "cota %d " %  b.cards['0_0'].timeout_cote
print "cota %d " %  b.cards['0_1'].timeout_cote

print b.cards['0_0']
print b.cards['0_1']
