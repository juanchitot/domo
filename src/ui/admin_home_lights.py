
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

from ui.templates.admin_home_lights_template import Ui_Form

from ui.home_map_scene import HomeMapScene
from ui.admin_tab import AdminTab

# from ui.domotica_client import DomoticaClient

from ui.docked_add_area import DockedAddArea

from PyQt4.QtCore import QCoreApplication     

class AdminHomeLights(AdminHomeModule,Ui_Form,AdminTab):
    
    MENU_KEY = 'ADMIN_HOME_LIGHTS'    
    
    def __init__(self):        
        
        AdminHomeModule.__init__(self)        
        self.setupUi(self)            
        
        self.home_map_scene = HomeMapScene.get_instance(self)               
        
        self.home_map_view.setScene(self.home_map_scene)
        #         self.last_click = None
        #         self.selection_started = False
        #         self.current_selection = []
        
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
        menu = QMenu(QCA.translate('AdminHomeLights' ,'Administrar Luces'),
                     self)
        
        action = QAction(QCA.translate('AdminHomeLights' ,'Agregar Luz'),menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.add_light)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeLights' ,'Mover Luz'), menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.move_light)            
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
    
    def add_light(self):
        self.abort_operation_mode()
        self.start_operation_mode('add_light',{'position':None })
    
    def _start_add_light(self):
        self.register_handler(self.home_map_scene,
                              QEvent.GraphicsSceneMouseRelease)        
        self.register_handler(self.home_map_scene,
                              QEvent.GraphicsSceneMousePress)        
    
    def _enter_add_light(self,event):       
        p = event.scenePos()
        self.current_op_stat['position'] = p
    
    def _finish_add_light(self):
        self.unregister_handler(self.home_map_scene,
                                QEvent.GraphicsSceneMouseRelease)
        self.unregister_handler(self.home_map_scene,
                                QEvent.GraphicsSceneMousePress)        
        
        p = self.current_op_stat['position']
        el_it = QGraphicsEllipseItem(p.x()-4,p.y()-4,8,8)
        
        HMItem.module(el_it, self.__class__.__name__)
        HMItem.type(el_it ,HMItem.ARTIFACT)
        HMItem.level(el_it, self.home_map_scene.current_level)
        
        el_it.setPen(QPen(Qt.blue,
                          1, 
                          Qt.SolidLine, 
                          Qt.RoundCap, 
                          Qt.RoundJoin))
        
        el_it.setBrush(QBrush(Qt.blue))
        el_it.setZValue(1)
        self.home_map_scene.addItem(el_it)
        
        self.current_op = ''
        self.current_op_stat = None          
    
    def move_light(self):
        super(AdminHomeLights,self).move_object(HMItem.ARTIFACT)
        
    # QEvent.GraphicsSceneMousePress        
    def event_handler_156(self,obj,event):
        if self.current_op == 'add_light':
            self.enter_operation_mode(event)
            return True
        else:
            return super(AdminHomeModule,self).event_handler_156(obj,event)
            
    #QEvent.GraphicsSceneMouseRelease
    def event_handler_157(self,obj,event):
        if self.current_op == 'add_light':
            self.leave_operation_mode()
            return True
        else:
            return super(AdminHomeModule,self).event_handler_157(obj,event)
        
                              

    
