
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
from ui.templates.admin_device_mapper_template import Ui_Form
from ui.admin_tab import AdminTab 

from ui.docked_add_area import DockedAddArea

from PyQt4.QtCore import QCoreApplication     

class AdminDeviceMapper(AdminHomeModule,Ui_Form,AdminTab):
    
    MENU_KEY = 'ADMIN_DEVICES'    
    
    def __init__(self):        
        
        AdminHomeModule.__init__(self)        
        self.setupUi(self)            
        
        #         self.home_map_scene = HomeMapScene.get_instance(self)               
        
        #         self.home_map_view.setScene(self.home_map_scene)
        #         self.last_click = None
        #         self.selection_started = False
        #         self.current_selection = []
        
        self.setup_connections()        
    
    def setup_connections(self):
        pass
        #         QObject.connect(self.home_map_scene, 
        #                         SIGNAL('levelAdded(int)'),                         
        #                         self.levels_box)                    
        #         QObject.connect(self.level_combo, 
        #                         SIGNAL('currentIndexChanged(QString)'), 
        #                         self.home_map_scene.set_current_level)        
    
    def initialize(self):
        print "initialize %d" % id(self)
    
    def build_menu(self):
        print self.parent().objectName()
        menu = QMenu(QCA.translate('AdminHomeLights' ,'Administrar Luces'),
                     self)
        
        #         action = QAction(QCA.translate('AdminHomeLights' ,'Agregar Luz'),menu)
        #         QtCore.QObject.connect(action, SIGNAL("triggered()"), self.add_light)            
        #         menu.addAction(action)
        
        #         action = QAction(QCA.translate('AdminHomeLights' ,'Mover Luz'), menu)
        #         QtCore.QObject.connect(action, SIGNAL("triggered()"), self.move_light)            
        #         menu.addAction(action)
        
        return menu
