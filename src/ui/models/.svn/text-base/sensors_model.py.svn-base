import yaml
from ui.client_core import ClientCore
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt4 import QtCore

class SensorsModel(QAbstractTableModel):
    def __init__(self,parent):
        QAbstractTableModel.__init__(self,parent)
        
        self.sensors_ports_keys = []
        self.sensors_ports = []        
        self.client_core = ClientCore.get_instance()
        self.setup_connections()
        
    def setup_connections(self):
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL("connected()"), 
                               self.update_status)        
        
    def update_status(self):
        self.sensors_ports = self.client_core.get_in_ports()
        self.sensors_ports_keys = self.sensors_ports.keys()
#         print "hago un get_in_ports"
#         print yaml.dump(self.sensors_ports)
        self.emit(QtCore.SIGNAL('modelReset()'))
        
    def rowCount(self,index):
        if not index.isValid():
            return len(self.sensors_ports_keys)
        return 0
    
    def columnCount(self,index):
        if not index.isValid():
            return 1
        return 0
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        key = self.sensors_ports_keys[index.row()]
        return QVariant(key)    
    
