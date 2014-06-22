
from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import QWidget, \
    QApplication, \
    QHeaderView, \
    QAbstractItemView, \
    QRegExpValidator, \
    QFileDialog, \
    QPixmap, \
    QPolygonF, \
    QPen, \
    QBrush, \
    QAction, \
    QMenuBar, \
    QMenu, \
    QInputDialog, \
    QGraphicsItem ,\
    QGraphicsEllipseItem, \
    QGraphicsPolygonItem, \
    QMessageBox

from PyQt4.QtCore import QVariant, \
    QEvent, \
    QObject, \
    QString, \
    Qt, \
    QString, \
    QRegExp, \
    QDir, \
    QStringList, \
    QCoreApplication as QCA, \
    QObject, \
    SIGNAL

from ui.home_map_item import HMItem
from ui.admin_home_module import AdminHomeModule
from ui.home_heating import HomeHeating

from ui.templates.admin_home_heating_template import Ui_Form

from ui.home_map_scene import HomeMapScene
from ui.admin_tab import AdminTab

from ui.custom_items.temperature_item import TemperatureItem

# from ui.domotica_client import DomoticaClient

from ui.docked_add_area import DockedAddArea

from PyQt4.QtCore import QCoreApplication     

class AdminHomeHeating(AdminHomeModule,Ui_Form,AdminTab):
    
    MENU_KEY = 'ADMIN_HOME_HEATING'    
    
    def __init__(self):        
        
        AdminHomeModule.__init__(self)        
        AdminHomeModule.initialize(HomeHeating,self)
        
        self.setupUi(self)            
        
        self.home_map_scene = HomeMapScene.get_instance(self)               
        
        self.home_map_view.setScene(self.home_map_scene)
        self.setup_connections()        
    
    def setup_connections(self):
        QObject.connect(self.home_map_scene, 
                        SIGNAL('levelAdded(int)'),                         
                        self.levels_box)                    
        QObject.connect(self.level_combo, 
                        SIGNAL('currentIndexChanged(QString)'), 
                        self.home_map_scene.set_current_level)        
    
    def initialize(self):
        print "initialize %d" % id(self)
    
    def build_menu(self):
        print self.parent().objectName()
        menu = QMenu(QCA.translate('AdminHomeHeating' ,'Administrar Climatizacion'),
                     self)
        
        action = QAction(QCA.translate('AdminHomeHeating' ,'Agregar Display'),menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.add_display)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeHeating' ,'Mover Display'), menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.move_display)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeHeating' ,'Iniciar'), menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.home_module.startTimer)            
        menu.addAction(action)

        action = QAction(QCA.translate('AdminHomeHeating' ,'Detener'), menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.home_module.killTimer)            
        menu.addAction(action)
        
        return menu
    
    def levels_box(self,level=None):
        if level:
            level_str = QString('Nivel %d' % level)
            self.level_combo.addItem(level_str)
            level_index = self.level_combo.findText(level_str)
            self.level_combo.setCurrentIndex(level_index)
        else:
            self.level_combo.clear()        
            l = self.home_map_scene.levels_availables
            self.level_combo.addItems([ QCA.translate('AdminHomeMap' ,'Nivel %1').arg(level) 
                                        for level in l ])
    
    def add_display(self):
        analog_ports = self.home_module.client_core.get_analog_ports()
        
        (name,ok) = QInputDialog.getText(self,
                                         QCA.translate('AdminHomeMap', "Agregar Display"),
                                         QCA.translate('AdminHomeMap', 'Ingresar el nombre del display:'))
        
        if ok :
            if len(name) > 32 or len(name) < 3:
                QMessageBox.critical(self,
                                     QCA.translate('AdminHomeHeating', "Agregar Display"),
                                     QCA.translate('AdminHomeHeating', "El nombre del display debe tener entre 3 y 32 caracteres"))
            else:                
                (port,ok) = QInputDialog.getItem(self,
                                                 QCA.translate('AdminHomeHeating', "Seleccionar puerto"),
                                                 QCA.translate('AdminHomeHeating', "Seleccionar el puerto del display"),
                                                 analog_ports.keys(),
                                                 0,
                                                 False)
                
                self.abort_operation_mode()
                self.start_operation_mode('add_display',{'position': None,
                                                         'name': name,
                                                         'port': port })
    
    def _start_add_display(self):
        self.register_handler(self.home_map_scene,
                              QEvent.GraphicsSceneMouseRelease)        
        self.register_handler(self.home_map_scene,
                              QEvent.GraphicsSceneMousePress)        
    
    def _enter_add_display(self,event):       
        p = event.scenePos()
        self.current_op_stat['position'] = p
    
    def _finish_add_display(self):
        self.unregister_handler(self.home_map_scene,
                                QEvent.GraphicsSceneMouseRelease)
        self.unregister_handler(self.home_map_scene,
                                QEvent.GraphicsSceneMousePress)        
        
        name = self.current_op_stat['name']        
        p = self.current_op_stat['position']
        port = self.current_op_stat['port'] 
        
        temp = TemperatureItem()
        temp.setTemperature(0)   
        temp.setPos(p)        
        temp.setToolTip(name)
        
        self.home_map_scene.addItem(temp)        
        HMItem.name(temp, name)
        HMItem.module(temp, self.__class__.__name__)
        HMItem.type(temp ,HMItem.ARTIFACT)
        HMItem.level(temp, self.home_map_scene.current_level)
        HMItem.ports(temp, 'In', [port] )
        
        item_key = 'name_%d' % (len(self.home_module.artifacts))
        self.home_module.artifacts[item_key] = temp
        
        self.current_op = ''
        self.current_op_stat = None          
    
    def move_display(self):
        super(self.__class__,self).move_object(HMItem.ARTIFACT)
    
    # QEvent.ToolTip
    def event_handler_110(self,obj,event):
        print "focus %s " % QApplication.focusWidget()
        print obj
        wid = obj.widget()
        print "tooltip 1 %s " % obj.toolTip()
        print "tooltip 2 %s " %  wid.toolTip()
        print "enabled 1 %s " % obj.isEnabled()
        print "enabled 2 %s " %  wid.isEnabled()
        print "visible 1 %s " % obj.isVisible()
        print "visible 2 %s " %  wid.isVisible()
        print "flags %x" % obj.flags()
        
        print "entro a event_handler_127"
        return False
    
    # QEvent.HoverEnter
    def event_handler_127(self,obj,event):
        print "focus %s " % QApplication.focusWidget()
        print obj
        print "tooltip 1 %s " % obj.toolTip()
        print "tooltip 2 %s " %  wid.toolTip()
        print "enabled 1 %s " % obj.isEnabled()
        print "enabled 2 %s " %  wid.isEnabled()
        print "visible 1 %s " % obj.isVisible()
        print "visible 2 %s " %  wid.isVisible()
        print "flags %x" % obj.flags()
        
        print "entro a event_handler_127"
        return False
    
    # QEvent.GraphicsSceneHoverMove
    def event_handler_161(self,obj,event):
        print "focus %s " % QApplication.focusWidget()
        print obj
        print "tooltip 1 %s " % obj.toolTip()
        print "tooltip 2 %s " %  wid.toolTip()
        print "enabled 1 %s " % obj.isEnabled()
        print "enabled 2 %s " %  wid.isEnabled()
        print "visible 1 %s " % obj.isVisible()
        print "visible 2 %s " %  wid.isVisible()
        print "flags %x" % obj.flags()
        
        print "entro a event_handler_161"
        return False
    
    # QEvent.GraphicsSceneHoverEnter
    def event_handler_160(self,obj,event):
        print "focus %s " % QApplication.focusWidget()
        print obj
        wid = obj.widget()
        print "tooltip 1 %s " % obj.toolTip()
        print "tooltip 2 %s " %  wid.toolTip()
        print "enabled 1 %s " % obj.isEnabled()
        print "enabled 2 %s " %  wid.isEnabled()
        print "visible 1 %s " % obj.isVisible()
        print "visible 2 %s " %  wid.isVisible()
        print "flags %x" % obj.flags()
        
        print "entro a event_handler_160"
        return False
        
    # QEvent.GraphicsSceneMousePress        
    def event_handler_156(self,obj,event):
        if self.current_op == 'add_display':
            self.enter_operation_mode(event)
            return True
        else:
            return super(self.__class__,self).event_handler_156(obj,event)
            
    #QEvent.GraphicsSceneMouseRelease
    def event_handler_157(self,obj,event):
        if self.current_op == 'add_display':
            self.leave_operation_mode()
            return True
        else:
            return super(self.__class__,self).event_handler_157(obj,event)
        
                              

    
