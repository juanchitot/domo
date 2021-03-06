from PyQt4.QtGui import QWidget, \
    QGraphicsView, \
    QGraphicsScene, \
    QTransform

from PyQt4.QtCore import QEvent, \
    Qt, \
    QString, \
    QObject, \
    SIGNAL

from PyQt4 import QtGui, \
    QtCore


from ui.templates.home_map_template import Ui_Form
from ui.home_module import HomeModule
from ui.client_core import ClientCore
from ui.home_map_scene import HomeMapScene
import time

class HomeMap(HomeModule,Ui_Form):
    

    
    def __init__(self,parent):
        
        HomeModule.__init__(self)        
        
        self.setupUi(self)                
        self.client_core = ClientCore.get_instance()
        self.initialized = False        
        self.startTimer(1000)
        self.home_map_scene = HomeMapScene.get_instance(self.graphicsView)
        self.graphicsView.setScene(self.home_map_scene)
        self.setup_connections()
        self.last_zoom = 100
        
    def setup_connections(self):
        QObject.connect(self.home_map_scene, 
                        SIGNAL('levelAdded(int)'), 
                        self.levels_box)        
        QObject.connect(self.level_combo, 
                        SIGNAL('currentIndexChanged(QString)'), 
                        self.home_map_scene.set_current_level)        
        QObject.connect(self.map_zoom, 
                        SIGNAL('valueChanged(int)'), 
                        self.set_zoom)        
        QObject.connect(self.map_zoom, 
                        SIGNAL('valueChanged()'), 
                        self.set_zoom)        

        
    def event(self,event):
        if event.type() == QEvent.Show :
            self.client_core.start_timer()
            return True
        if event.type() == QEvent.Timer :
            self.timerEvent(event)
        return False
    
    def timerEvent(self,t_ev):        
        self.time_lcd.display(time.strftime('%H:%M:%S'))
    
    def move_box(self):
        pass    
    
    def levels_box(self,level=None):
        if level:
            level_str = QString('Nivel %d' % level)
            self.level_combo.addItem(level_str)
            level_index = self.level_combo.findText(level_str)
            self.level_combo.setCurrentIndex(level_index)
        else:
            self.level_combo.clear()        
            l = self.home_map_scene.levels_availables
            self.level_combo.addItems([ QString('Nivel %d' % level) for level in l ])
            
    def set_zoom(self,zoom=None):
        max = self.map_zoom.maximum()
        min = self.map_zoom.minimum()
        
        self.graphicsView.resetTransform()
               
        if not zoom is None:            
            self.zoom_lab.setText('%d%%' % zoom)
            
            n_z = zoom/100.0
            self.graphicsView.scale(n_z,n_z)
            self.last_zoom = zoom

