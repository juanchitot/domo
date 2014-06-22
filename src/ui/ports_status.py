import yaml
from PyQt4 import QtCore

from PyQt4.QtGui import QWidget, QTableWidget,QTableWidgetItem, QLabel
from PyQt4.QtCore import QVariant, \
    QSize, \
    QPoint, \
    QRect, \
    QTimer, \
    QObject

from PyQt4.QtGui import QVBoxLayout

from ui.templates.ports_status_template import Ui_Form
from ui.digital_card_status import DigitalCardStatus
from ui.analogic_card_status import AnalogicCardStatus
from ui.debug_card_status import DebugCardStatus

from ui.client_core import ClientCore

class PortsStatus(QWidget,Ui_Form):
    def __init__(self):
        
        QWidget.__init__(self)
        self.setupUi(self)
        self.client_core = ClientCore.get_instance()
        self.tab_position = 1
        
        self.cards = {}
        
        self.initialized = False
        self.update_ports_timer = None
        
        QObject.connect(self.client_core, 
                        QtCore.SIGNAL("connectionClosed()"), 
                        self.reset_status)        
        QObject.connect(self.client_core, 
                        QtCore.SIGNAL("cardsAdded()"), 
                        self.update_status)        
        
        
    def tab_changed(self):
        if self == self.parentWidget().currentWidget() :
            self.start_pooling()            
        else:
            self.stop_pooling()
            
    def start_pooling(self):
        self.update_ports_timer = self.startTimer(1000)
        if not self.initialized:
            self.initialized = True
            self.load_tables()
    
    def timerEvent(self,event):
        self.client_core.get_all_ports()
        self.emit(QtCore.SIGNAL('timeout()'))
    
    def focusInEvent(self,event):
        pass
#         print "sucedio el evento %s %s" % (event.type(), str(event))                  
        
    def focusOutEvent(self,event):
        pass
#         print "sucedio el evento %s %s" % (event.type(), str(event))                  
    
    def stop_pooling(self):
        if self.update_ports_timer :
            self.killTimer(self.update_ports_timer)   
    
    def add_digital_card_table(self, card_id=None ):        
        cards_len = len(self.cards)
        
        dig = DigitalCardStatus(self,card_id)                
        self.cards[card_id] = dig        
        
        self.cards_table.addWidget(dig)
#         print "hice un addwidget en cards table %d " % self.cards_table.count()
        
        QObject.connect(self,
                        QtCore.SIGNAL("timeout()"), 
                        dig.update_ports)
    
    def add_debug_card_table(self, card_id=None ):        
        cards_len = len(self.cards)
        
        deb = DebugCardStatus(self,card_id)                
        self.cards[card_id] = deb        
        
        self.cards_table.addWidget(deb)
        #         #         print "hice un addwidget en cards table %d " % self.cards_table.count()        
        QObject.connect(self,
                        QtCore.SIGNAL("timeout()"), 
                        deb.update_ports)
        
    def add_analogic_card_table(self, card_id=None ):        
        cards_len = len(self.cards)
        
        ana = AnalogicCardStatus(self,card_id)                
        self.cards[card_id] = ana        
        
        self.cards_table.addWidget(ana)
#         print "hice un addwidget en cards table %d " % self.cards_table.count()        
        QObject.connect(self, 
                        QtCore.SIGNAL("timeout()"), 
                        ana.update_ports)
        
    def load_tables(self):        
        cards = self.client_core.get_cards()        
        
        for c_id, c_attrs in cards.items():
            if c_attrs['type'] == 'Analogic':
                self.add_analogic_card_table(c_id)
            elif c_attrs['type'] == 'DebugCard':
                self.add_debug_card_table(c_id)
            else:
                self.add_digital_card_table(c_id)
    
    def clear_cards_tables(self):
        table = self.cards_table
        count = table.count()
        while count > 0:
            item = table.itemAt(count-1)
            wid = item.widget()
            QObject.disconnect(wid,0,0,0)
            wid.deleteLater()
            count -= 1
            
    def reset_status(self):
        self.stop_pooling()
        self.clear_cards_tables()
        self.initialized = False
        
    def update_status(self):
#         print 'entro en update_status'
        self.reset_status()
        self.tab_changed()
