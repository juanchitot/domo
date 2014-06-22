import yaml
import re

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication, QHeaderView, QAbstractItemView, QRegExpValidator
from PyQt4.QtCore import QVariant, QEvent, QObject, QString, Qt, QRegExp

from ui.templates.admin_light_template import Ui_Form

from PyQt4.QtGui import QVBoxLayout, QTableWidgetItem, QPushButton, QStandardItemModel, QStandardItem, QDirModel
# from PyQt4.Qwt5 import QwtDial

from ui.client_core import ClientCore
from interface.light_map import LightMap
from ui.models.light_map_model import LightMapModel
from ui.models.ports_model import PortsModel

from datetime import timedelta

class AdminLight(QWidget,Ui_Form):
    
    def __init__(self):
        
        QWidget.__init__(self)
        self.setupUi(self)                
        
        self.client_core = ClientCore.get_instance()
        self.initialized = False
        self.hide_errors()        
        
        self.light_map_model = LightMapModel(self)                
        
        self.ports_in = PortsModel(self)
        self.ports_out = PortsModel(self)       
        
        self.ports_in.filter_card_type([PortsModel.DIGITAL_CARD,PortsModel.DEBUG_CARD])
        self.ports_out.filter_card_type([PortsModel.DIGITAL_CARD,PortsModel.DEBUG_CARD])
        
        self.ports_in.filter_port_type(PortsModel.IN_PORT)         
        self.ports_out.filter_port_type(PortsModel.OUT_PORT)
        
        
        self.sensors_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lights_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.light_maps_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.sensors_view.setModel(self.ports_in)        
        self.lights_view.setModel(self.ports_out)        
        
        self.light_maps_table.setModel(self.light_map_model)
        
#         self.set_validators()       
        QtCore.QObject.connect(self.client_core,
                               QtCore.SIGNAL("connectionClosed()"),
                               self.reset_status)
        QtCore.QObject.connect(self.client_core,
                               QtCore.SIGNAL("cardsAdded()"),
                               self.update_status)
        QtCore.QObject.connect(self.client_core,
                               QtCore.SIGNAL("connected()"),
                               self.tab_changed)
        QtCore.QObject.connect(self.lights_view,
                               QtCore.SIGNAL("pressed(QModelIndex)"),
                               self.ports_out.toggle_port)
        QtCore.QObject.connect(self.sensors_view,
                               QtCore.SIGNAL("pressed(QModelIndex)"),
                               self.ports_in.toggle_port)
        
    def set_validators(self):
        timedelta_v = QRegExpValidator(QRegExp(LightMapModel.RE_TIMEDELTA)
                                       ,self)
        self.map_timeout.setValidator(timedelta_v)
        self.map_delay.setValidator(timedelta_v)
    
    def parse_combos(self):
        sensors_indexes = self.sensors_view.selectedIndexes()
        lights_indexes = self.lights_view.selectedIndexes()
        
        sensors = {}
        for index in sensors_indexes:
            if index.column() > 0 :
                continue
            else:
                key = str(index.data().toString())
                type_index = self.ports_in.createIndex(index.row(),1)
                
                type = False
                if type_index.data().toString() == PortsModel.PORT_OPEN:
                    type = True
                
                sensors[key] = type
        
        lights = {}
        for index in lights_indexes:
            if index.column() > 0 :
                continue
            else:
                key = str(index.data().toString())
                type_index = self.ports_out.createIndex(index.row(),1)
                
                type = False
                if type_index.data().toString() == PortsModel.PORT_OPEN:
                    type = True
                
                lights[key] = type
                
        return (sensors,lights)
        
    def add_light_map(self):
        
        title = str(self.map_title.text())
        comment = str(self.map_comment.document().toPlainText())
        
        if not title or not comment:
            self.set_error("Ingrese un titulo y un comentario para el map")
            return
        
        selection = self.parse_combos()
        
        if not len(selection[0]) or not len(selection[1]):
            self.set_error("Seleccione un puerto para la luz, y para el sensor")
            return
        
        if len(selection[0]) > 10  or len(selection[1]) > 10:
            self.set_error("La cantidad de sensores o luces maxima es 10")
            return
        
        timeout = str(self.map_timeout.text())
        delay = str(self.map_delay.text())        
        
        match =re.match(LightMapModel.RE_TIMEDELTA,timeout)
        timedelta_map = {}
        if match:
            timedelta_map = match.groupdict()
            timedelta_map['microseconds'] = 0
            for k in timedelta_map.keys():
                if not timedelta_map[k]:
                    timedelta_map[k] = 0
                else:
                    timedelta_map[k] = int(timedelta_map[k])
        timeout = timedelta(**timedelta_map)         
        
        match = re.match(LightMapModel.RE_TIMEDELTA,delay)
        timedelta_map = {}
        if match:
            timedelta_map = match.groupdict()
            timedelta_map['microseconds'] = 0
            for k in timedelta_map.keys():
                if not timedelta_map[k]:
                    timedelta_map[k] = 0
                else:
                    timedelta_map[k] = int(timedelta_map[k])
        delay = timedelta(**timedelta_map)         
        
        
        lm = LightMap()
        lm.name = title
        lm.comment = comment
        lm.sensors_ports = selection[0]
        lm.light_ports = selection[1]
        lm.timeout = timeout
        lm.delay = delay
        
        ret_lm = self.client_core.add_light_map(lm)
    
    def showEvent(self,event):
        self.tab_changed()
    
    def hide_errors(self):
        self.error_msg.hide()
        
    def set_error(self,error_msg):
        self.error_msg.setText(error_msg)
        self.error_msg.show()
    
    def tab_changed(self):
        if self == self.parentWidget().currentWidget() :
            if not self.initialized:
                self.initialize()
        self.sensors_view.resizeColumnsToContents()        
        self.lights_view.resizeColumnsToContents()
        self.sensors_view.horizontalHeader().hide()
        self.lights_view.horizontalHeader().hide()
    
    def update_status(self):
        self.initialize()
    
    def reset_status(self):        
        count = self.light_maps_table.rowCount()
        self.initialized = False
        self.map_sensor_combo.clear()
        self.map_light_combo.clear()        
    
    def initialize(self):
        self.initialized = True
#         self.client_core.connect()
    
    def del_light_map(self):        
        lists = self.light_maps_table.selectedIndexes()
        rows = []
        for index in lists:
            if index.column() == 0:
                rows.append(index.row())
        self.light_map_model.removeIndexes(rows)
