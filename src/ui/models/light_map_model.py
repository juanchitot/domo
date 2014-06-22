import yaml
import string
import re

from datetime import timedelta

from ui.client_core import ClientCore

from PyQt4 import QtCore
from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import Qt, QModelIndex, QVariant

from interface.light_map import LightMap

class LightMapModel(QAbstractTableModel):
    
    NAME_COLUMN = 0 
    TIMEOUT = 1
    DELAY = 2
    LIGHTS_PORTS = 3
    SENSORS_PORTS = 4
    COMMENT = 5
    SENSOR_TYPE = 6
    
    RE_TIMEDELTA = '^((?P<days>\d{1,2}),)??((?P<hours>\d{1,2}),)??((?P<minutes>\d{1,2}),)??(?P<seconds>\d{1,6})?(:{1}(?P<milliseconds>\d{0,3}){1})??$'
    
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self,parent)
        
        self.client_core = ClientCore.get_instance()        
        
        self.headers = [('name',QVariant('Titulo')),
                        ('timeout',QVariant('Timeout')),
                        ('delay',QVariant('Delay')),
                        ('light_ports',QVariant('Luz')),
                        ('sensors_ports',QVariant('Sensor')),
#                         ('sensor_type',QVariant('Tipo')),
                        ('comment',QVariant('Comentario'))]
        self.lmps = {}        
        self.lmps_keys = []
        self.root_node = QModelIndex()
        
        self.setup_connections()
        
    def setup_connections(self):
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL('lightMapChange()'), 
                               self.update_status)        
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL("connected()"), 
                               self.update_status)  
        
# LM_12505445752374410: !LightMap
# - []
# - comment: test
#   delay: 0
#   events_actions:
#   - [CE_12505445752369570, 12505445752369810]
#   - [CE_12505445752372660, 12505445752372798]
#   id: LM_12505445752374410
#   light_ports: [Bus_0_O_02_00]
#   name: test
#   sensor_type: close
#   sensors_ports: [Bus_0_I_02_00]
#   timeout: 10  
    def update_status(self):
        self.lmps = self.client_core.get_light_maps()
        self.lmps_keys = self.lmps.keys()
        self.emit(QtCore.SIGNAL('modelReset()'))
        
    def rowCount(self,parent):
        return len(self.lmps_keys)
    
    def columnCount(self,parent):
        return len(self.headers)
    
    def data(self,index,role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        
        row = index.row()
        column = index.column()
        if row < len(self.lmps_keys) and column < len(self.headers):
            lmp = self.lmps[self.lmps_keys[row]]
            attr = getattr(lmp,self.headers[column][0])
            
            if column in [self.LIGHTS_PORTS,self.SENSORS_PORTS] :
                str_attr = ''
                for k, status in attr.items():
                    str_attr += "(%s:%s)\n" % (k,
                                               'Cerrado' if not status else 'Abierto' )                    
                attr = str_attr                    
            elif column in [self.DELAY,self.TIMEOUT]:
                attr = "%d,%d,%d,%d:%d" % (attr.days,
                                           attr.seconds/3600,
                                           ((attr.seconds%3600)/60),
                                           attr.seconds % 60,
                                           attr.microseconds/1000)
            return QVariant(attr)
            
        return QVariant()
    
    def setData(self,index, value, role=Qt.EditRole):
        if not index.isValid() and role != Qt.EditRole :
            return False
        
        lmp = self.lmps[self.lmps_keys[index.row()]]
        
        if index.column() == self.TIMEOUT:
            val = str(value.toString())
            match = re.match(self.RE_TIMEDELTA,val)
#             print match
            if match:
                timedelta_map = match.groupdict()
                timedelta_map['microseconds'] = 0
                for k in timedelta_map.keys():
                    if not timedelta_map[k]:
                        timedelta_map[k] = 0
                    else:
                        timedelta_map[k] = int(timedelta_map[k])
                        
#                 print timedelta_map
                lmp.timeout = timedelta(**timedelta_map)         
#                 print lmp.timeout
                self.client_core.edit_light_map(lmp)
                self.update_status()
                return True
            
        if index.column() == self.DELAY:
            
            val = str(value.toString())
            match =re.match( self.RE_TIMEDELTA,val)
#             print match
            if match:
                timedelta_map = match.groupdict()
                timedelta_map['microseconds'] = 0
                for k in timedelta_map.keys():
                    if not timedelta_map[k]:
                        timedelta_map[k] = 0
                    else:
                        timedelta_map[k] = int(timedelta_map[k])
                        
#                 print timedelta_map
                lmp.delay = timedelta(**timedelta_map)            
#                 print lmp.delay
                self.client_core.edit_light_map(lmp)
                self.update_status()
                return True    
        if index.column() == self.NAME_COLUMN:
            val = value.toString()
            if not len(val):
                return False
            lmp.name = val
            self.client_core.edit_light_map(lmp)
            self.update_status()
            return True    
        if index.column() == self.COMMENT:            
            val = value.toString()
            if not len(val):
                return False
            lmp.comment = val
            self.client_core.edit_light_map(lmp)
            self.update_status()
            return True    

        return False
            
    def flags(self,index):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() in [self.DELAY,self.TIMEOUT,self.NAME_COLUMN,self.COMMENT] :
            return Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsEnabled
        
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled
    
    def headerData(self,section,orientation,role=Qt.DisplayRole):
        if role != Qt.DisplayRole:            
            return QVariant()
        if section < len( self.headers) and orientation == Qt.Horizontal:
            return QVariant(self.headers[section][1])
        if Qt.Vertical and section < len(self.lmps_keys):
            return QVariant(section)        
        return QVariant()
    
    
    def removeIndexes(self, rows):
        lm_to_del = []
        for row in rows:
            lm_to_del.append(self.lmps[ self.lmps_keys[row] ])
        self.client_core.del_light_map(lm_to_del)
        self.update_status()
        
            
            
