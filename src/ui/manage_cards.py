import re

import yaml

from PyQt4.QtGui import QWidget, \
    QTableWidgetItem, \
    QPushButton

from PyQt4 import QtCore

from PyQt4.QtCore import QVariant

from ui.templates.manage_cards_template import Ui_Form
from ui.client_core_exception import ClientCoreException
from ui.client_core import ClientCore

class ManageCards(QWidget,Ui_Form):
    
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        
        self.client_core = ClientCore.get_instance()
        
        self.initialized = False
        self.hide_errors()
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL("connectionClosed()"), 
                               self.reset_status)        
    
    
    def initialize(self):
        self.client_core.get_cards()
        channels =  self.client_core.channels
        
        for ch, ch_itm in channels.items():            
            for cd, cd_itm in ch_itm.items():
                rows = self.cards_table.rowCount()
                self.cards_table.insertRow(rows)
                
                id = QTableWidgetItem(cd_itm['card_id'])
                self.cards_table.setItem(rows,0,id)
                
                serial = QTableWidgetItem(cd_itm['channel_id'])
                self.cards_table.setItem(rows,1,serial)
                
                type = QTableWidgetItem(cd_itm['type'])
                self.cards_table.setItem(rows,2,type)
                
                but = self._get_remove_card_button(rows)
                self.cards_table.setCellWidget(rows,3,but)
                QtCore.QObject.connect(but, 
                                       QtCore.SIGNAL("pressed()"), 
                                       self.remove_card)
                
        self.initialized = True        
    
    def add_card(self):
        self.add_card_but.setDisabled(True)
        if self.card_type_cmb.currentIndex() == 0 :
            card_type = 'Digital'
        elif self.card_type_cmb.currentIndex() == 1 :
            card_type = 'Analogic'
        else :
            card_type = 'DebugCard'
        
        #         Validacion Bus y Address
        addr_edit = self.addr_edit.displayText().toLatin1()
        m = re.match("^([0-9]{0,1}[02468])$", addr_edit )
        if m:
            addr_edit = int(m.group(0))
        else:
            self.addr_edit_error.show()
            self.add_card_but.setDisabled(False)
            return
        
        channel_edit = self.channel_edit.displayText().toLatin1()
        m = re.match("^([0-9]{1})$", channel_edit )
        if m:
            channel_edit = int(m.group(0))
        else:
            self.channel_edit_error.show()
            self.add_card_but.setDisabled(False)
            return
#         fin validacion
        
        try :
            self.client_core.add_card(addr_edit,channel_edit,card_type)
        except Exception, e:
            self.inform_error(e.message)
            self.addr_edit.setText('')
            self.channel_edit.setText('')
            self.add_card_but.setDisabled(False)
        else:
            self.clear_cards_table()
            self.initialize()
            self.addr_edit.setText('')
            self.channel_edit.setText('')
            self.add_card_but.setDisabled(False)
            
    def tab_changed(self):
        if self == self.parentWidget().currentWidget() :
            if not self.initialized:
                self.initialize()
    
    def inform_error(self,msg):
        self.error_msg.setText(msg)
        self.error_msg.show()
        
    def hide_errors(self):        
        self.addr_edit_error.hide()
        self.channel_edit_error.hide()
        self.error_msg.hide()
        
    def clear_cards_table(self):
        while self.cards_table.rowCount() > 0 :
            self.cards_table.removeRow( self.cards_table.rowCount()-1 )
    
    def remove_card(self):
        but = self.sender()
        row = but.property('row').toInt()[0]
        card_id = str(self.cards_table.item(row,0).text())
        self.client_core.remove_card(card_id)
        self.reset_status()
        self.initialize()
        
    def reset_status(self):
        self.hide_errors()
        self.initialized = False
        self.clear_cards_table()
    
    def search_connected_cards(self):
        channel = str(self.channel_cmb.currentIndex())
        try :
            ret = self.client_core.search_connected_cards(channel)
        except ClientCoreException, e:
            print "search_connected"
            self.channel_msg.setText(str(e))
        else:
            print "search_connected else"
            self.channel_msg.setText(ret)
                                   
    def _get_remove_card_button(self,row):
        but = QPushButton("X", self)
        but.setProperty('row',QVariant(row))
        return but
