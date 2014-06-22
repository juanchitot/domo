
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
from ui.templates.admin_home_map_template import Ui_Form
from ui.home_map_scene import HomeMapScene
from ui.admin_tab import AdminTab

# from ui.domotica_client import DomoticaClient

from ui.docked_add_area import DockedAddArea

from PyQt4.QtCore import QCoreApplication     

class AdminHomeMap(AdminHomeModule,Ui_Form,AdminTab):
    
    MENU_KEY = 'ADMIN_HOME_MAP'
    
    def __init__(self):        
        
        AdminHomeModule.__init__(self)        
        self.setupUi(self)            
        
        self.home_map_scene = HomeMapScene.get_instance(self)               
        
        self.home_map_view.setScene(self.home_map_scene)
        self.last_click = None
        self.selection_started = False
        self.current_selection = []
        
        self.setup_connections()
        
    
    def setup_connections(self):
        QObject.connect(self.home_map_scene, 
                        QtCore.SIGNAL("outlineMarked()"), 
                        self.clear_outline_points)
        # QObject.connect(self.home_map_scene,
        #                 QtCore.SIGNAL("outlinePoint(point)"),
        #                 self.set_outline_point)
        # QObject.connect(self.level_combo,
        #                 SIGNAL('currentIndexChanged(QString)'),
        #                 self.home_map_scene.set_current_level)
        # QObject.connect(self.home_map_scene,
        #                 SIGNAL('levelAdded(int)'),
        #                 self.levels_box)

    def initialize(self):
        print "initialize %d" % id(self)

    def build_menu(self):
        print self.parent().objectName()
        menu = QMenu(QCA.translate('AdminHomeMap' ,'Administrar Mapa'),
                     self)
        
        action = QAction(QCA.translate('AdminHomeMap' ,'Agregar Plano'),menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.add_map)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeMap' ,'Seleccionar Area'), menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.select_area)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeMap' ,'Demarcar Area'),menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.add_home_area)            
        menu.addAction(action)
        
        action = QAction(QCA.translate('AdminHomeMap' ,'Mover Area'),menu)
        QtCore.QObject.connect(action, SIGNAL("triggered()"), self.move_area)            
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


    def add_map(self):
        (level,ok) = QInputDialog.getInt(self,
                                         QCA.translate('AdminHomeMap' ,'Agregar plano'),
                                         QCA.translate('AdminHomeMap' ,'Nivel:'),
                                         0,-10,100)
        if ok : 
            
            overwrite = True 
            if self.home_map_scene.has_map(level) :
                ret = QMessageBox.question(self,
                                           QCA.translate('AdminHomeMap' ,'Mapa existente'),
                                           QCA.translate('AdminHomeMap' ,'El mapa ya existe desea sobrescribirlo'),
                                           QMessageBox.Yes| QMessageBox.No,
                                           QMessageBox.No)
                overwrite = (ret == QMessageBox.Yes)
            
            if overwrite :
                file = QFileDialog.getOpenFileName(self, 
                                                   QCA.translate('AdminHomeMap', "Seleccione la imagen del mapa"),
                                                   QDir.home().absolutePath(),
                                                   QCA.translate('AdminHomeMap',
                                                                 "Imagenes (*.bmp *.gif *.jpg *.jpeg *.png *.pbm *.pgm *.ppm *.xbm *.xpm)"))       
                if file:
                    self.home_map_scene.set_map(QPixmap(file),level)
                    self.home_map_view.update()               
                    
    def set_outline_point(self,p):        
        self.home_map_view.centerOn(p)       
        print "entro a outline point"
        self.selection_list.addItem("(%.0f : %.0f)" % (p.x(),p.y()))
        self.home_map_view.update()    

    def clear_outline_points(self):        
        self.selection_list.clear()            
    
    def add_home_area(self):        
        (name,ok) = QInputDialog.getText(self,
                                         QCA.translate('AdminHomeMap', "Agregar Mapa"),
                                         QCA.translate('AdminHomeMap', 'Ingresar el nombre del area:'))
        
        if ok :
            if len(name) > 32 or len(name) < 3:
                QMessageBox.critical(self,
                                     QCA.translate('AdminHomeMap', "Agregar Mapa"),
                                     QCA.translate('AdminHomeMap', "El nombre del area debe tener entre 3 y 32 caracteres"))
            else:
                self.add_area(name)
            
    def add_area(self,name):  
        self.abort_operation_mode()
        self.start_operation_mode('add_area', {'name': name, 'points': [] })
    
    def _start_add_area(self):
        
        self.register_handler(self.home_map_scene,
                              QEvent.GraphicsSceneMouseRelease)
        
        self.register_handler(self.home_map_scene,
                              QEvent.KeyRelease)        
        
    def _cancel_add_area(self):
        self.unregister_handler(self.home_map_scene,
                                QEvent.GraphicsSceneMouseRelease)
        
        self.unregister_handler(self.home_map_scene,
                                QEvent.KeyRelease)               
    def _update_add_area(self,event):
        p = event.scenePos()
        self.current_op_stat['points'].append(p)
        
        el_it = QGraphicsEllipseItem(p.x()-2,p.y()-2,4,4)
        
        HMItem.module(el_it,self.__class__.__name__)
        HMItem.type(el_it,HMItem.OUTLINE_POINT)
        HMItem.level(el_it, -1)
        el_it.setPen(QPen(Qt.black,
                          1, 
                          Qt.SolidLine, 
                          Qt.RoundCap, 
                          Qt.RoundJoin))
        el_it.setBrush(QBrush(Qt.Dense4Pattern))
        el_it.setZValue(1)
        self.home_map_scene.addItem(el_it)
    
    def _finish_add_area(self):    
        poligon = QPolygonF( self.current_op_stat['points'])        
        
        pol = QGraphicsPolygonItem(poligon)
        pol.setToolTip(self.current_op_stat['name'])
        pol.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))        
        
        HMItem.type(pol,HMItem.MAP_AREA)
        HMItem.select(pol,False)
        HMItem.name(pol,self.current_op_stat['name'])
        HMItem.level(pol, self.home_map_scene.current_level)
        
        pol.setVisible(True)
        pol.setZValue(1)
        
        

        self.home_map_scene.addItem(pol)        
        print "flags %x" % pol.flags()
        
        
        it_remove = QGraphicsPolygonItem()
        HMItem.module( it_remove, self.__class__.__name__)
        HMItem.type(it_remove,HMItem.OUTLINE_POINT)        
        self.home_map_scene.remove_by_item(it_remove)
        self.current_op = ''
        self.current_op_stat = None

    def move_area(self):
        super(AdminHomeMap,self).move_object(HMItem.MAP_AREA)
    
    #QEvent.KeyRelease
    def event_handler_7(self, obj, event):
        if event.key() == Qt.Key_Escape:
            self.abort_operation_mode()
        if event.key() == Qt.Key_Return:
            self.leave_operation_mode()
        return True

    
    #QEvent.GraphicsSceneMouseRelease
    def event_handler_157(self, obj, event):
        self.update_operation_mode(event)
        return True
    
    # QEvent.GraphicsSceneHoverEnter
    def event_handler_160(self,obj,event):
        print obj
        print "tooltip 1 %s " % obj.toolTip()
        print "enabled 1 %s " % obj.isEnabled()
        print "visible 1 %s " % obj.isVisible()
        print "flags %x" % obj.flags()
        
        print "entro a event_handler_160"
        return False
        
