import yaml
import re

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication, QHeaderView, QAbstractItemView, QRegExpValidator
from PyQt4.QtCore import QVariant, QEvent, QObject, QString, Qt, QRegExp

from ui.templates.admin_heating_maps_template import Ui_Form

from PyQt4.QtGui import QVBoxLayout, QTableWidgetItem, QPushButton, QStandardItemModel, QStandardItem, QDirModel


from ui.client_core import ClientCore
# from interface.light_map import LightMap
# from ui.models.light_map_model import LightMapModel
# from ui.models.ports_model import PortsModel

from datetime import timedelta

class AdminHeatingMaps(QWidget,Ui_Form):
    
    def __init__(self):
        
        QWidget.__init__(self)
        self.setupUi(self)                
    
    def tab_changed(self):
        pass
