import yaml
from ui.client_core import ClientCore
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt4 import QtCore

class PortsModel(QAbstractTableModel):
    
    PORT_CLOSED = 'Cerrado'
    PORT_OPEN = 'Abierto'
    
    DIGITAL_CARD = 'Digital'
    DEBUG_CARD = 'DebugCard'
    ANALOGIC_CARD = 'Analogic'
    
    IN_PORT = 'In'
    OUT_PORT = 'Out'
    
    def __init__(self,parent):
        QAbstractTableModel.__init__(self,parent)
        
        self.port_type_filter = None
        self.card_filter = None
        self.card_type_filter = None
        
        self.ports_keys = []
        self.ports = {}
        self.open_ports = []
        
        self.client_core = ClientCore.get_instance()
        self.setup_connections()
        
    def filter_port_type(self,type):
        self.port_type_filter = type
            
    def filter_cart(self,card):
        self.card_filter = card
    
    def filter_card_type(self,type):
        self.card_type_filter = type
    
    
    def setup_connections(self):
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL("connected()"), 
                               self.update_status)        
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL('cardsAdded()'), 
                               self.update_status)        
        QtCore.QObject.connect(self.client_core,                                
                               QtCore.SIGNAL("connectionClosed()"), 
                               self.reset_status)        

        
    def reset_status(self):
        self.ports.clear()
        del self.ports_keys[0:len(self.ports_keys)]
        self.emit(QtCore.SIGNAL('modelReset()'))
        
    def update_status(self):        
#         print "entro a update status de posts_model"
        if self.port_type_filter == self.IN_PORT :            
            self.ports = self.client_core.get_in_ports() 
        elif self.port_type_filter == self.OUT_PORT :
            self.ports = self.client_core.get_out_ports() 
        
        self.ports_keys = self.ports.keys()
        self.ports_keys.sort()  
        self.emit(QtCore.SIGNAL('modelReset()'))
    
    def rowCount(self,index):
        ret = 0
        if not index.isValid():
            ret = len(self.ports_keys)
        return ret
    
    def flags(self,index):
        if not index.isValid():
            return 0
        
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 1:            
            flags = Qt.ItemIsUserCheckable | flags 
        return flags
    
    def columnCount(self,index):
        if not index.isValid():
            return 2
#         print "retorno columncount 0"
        return 0
    
    def toggle_port(self,index):
        
        if index.isValid():
            if ( index.flags() & Qt.ItemIsUserCheckable ) :
                key = self.ports_keys[index.row()]
                if not key in self.open_ports:
                    self.open_ports.append(key)
                else:
                    self.open_ports.remove(key)
        self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'),
                  index,
                  index)
    
    def data(self, index, role=Qt.DisplayRole):
#         print "entro a data con %d %d" % (index.row(),
#                                               index.column())
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        key = self.ports_keys[index.row()]
        if index.column() == 0:
            value = key
        else:
            if key in self.open_ports :
                value = self.PORT_OPEN                
            else:
                value = self.PORT_CLOSED
                
        return QVariant(value)
    
#     def setData(self,index,value,role):
#         if not index.isValid() or role != Qt.DisplayRole or index.column() <> 1:
#             return false
        
#         return true
        
