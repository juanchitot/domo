
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDockWidget, \
    QApplication, \
    QCloseEvent

from PyQt4.QtCore import  QRect, QString
from ui.templates.floating_window_template import Ui_DockWidget
from ui.client_core import ClientCore
from PyQt4.QtGui import QVBoxLayout, QTableWidgetItem, QPushButton, QStandardItemModel, QStandardItem, QDirModel, QTreeView
# from PyQt4.Qwt5 import QwtKnob

class FloatingWindow(QDockWidget,Ui_DockWidget):
    
    def __init__(self,parent):
        QDockWidget.__init__(self,parent)
        self.setVisible(False)
        self.setupUi(self)
        self.client_core = ClientCore.get_instance()
        
        QtCore.QObject.connect(self.close_button, 
                               QtCore.SIGNAL("clicked()"), 
                               self.close)        
        QtCore.QObject.connect(self.connect_button, 
                               QtCore.SIGNAL("clicked()"), 
                               self.connect)
        QtCore.QObject.connect(self.client_core, 
                               QtCore.SIGNAL("connectionClosed()"), 
                               self.connect_window)
        


        
    def show_msg(self):        
#         self.msg_text = QwtKnob(self.dockWidgetContents)
#         self.gridLayout.addWidget(self.msg_text, 1, 1, 1, 2)
        msg = self.client_core.last_error
        self.msg_text.setText(msg)
        
    def connect(self):
        self.setVisible(True)
        parent = self.parentWidget()
        parent.setEnabled(True)
        self.hide()
        self.setEnabled(False)
        host = self.domotica_host.text()
        self.client_core.set_domotica_server(str(host))
        self.client_core.connect()
        
    def closeEvent(self,event):
        pr = self.parentWidget()
        pr.closeEvent(QCloseEvent(event))
        
    def connect_window(self):
        self.center()
        
        parent = self.parentWidget()
        parent.setEnabled(False)
        self.setEnabled(True)
        
        host = self.client_core.get_domotica_server()        
        self.domotica_host.setText(host)        
        self.show_msg()
        self.center()
        
        self.show()
        
    def center(self):               
        width = self.size().width()
        height = self.size().height()
        
        ap = QApplication.desktop()
        
        sc_width = ap.screenGeometry().width()
        sc_height = ap.screenGeometry().height()
        
        dock_pos_x = int(sc_width/2) - int(width/2)
        dock_pos_y = int(sc_height/2) - int(height/2)
        
        self.setGeometry(QRect(dock_pos_x,dock_pos_y,width,height))
