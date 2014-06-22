
from core.singleton_core import Singleton

from ui.home_map_item import HMItem
from ui.home_heating import HomeHeating

from PyQt4.QtGui import QWidget, \
    QGraphicsView, \
    QGraphicsScene, \
    QGraphicsPixmapItem, \
    QPolygonF, \
    QPen, \
    QBrush, \
    QGraphicsEllipseItem, \
    QGraphicsPolygonItem

from PyQt4 import QtGui, \
    QtCore

from PyQt4.QtCore import QEvent, \
    Qt, \
    QVariant, \
    SIGNAL

import re

class HomeMapScene(Singleton,QGraphicsScene):
    
    instance = None
    MAP_ITEM_NAME = 'HOME MAP LEVEL %d'
    
    #selection types
    SELECT_NONE = 0
    SELECT_POINT = 1
    OUTLINE_POINT = 2
    SELECT_MAP_AREA = 3
    
    
    def __init__(self,parent):
        QGraphicsScene.__init__(self,parent)
        self.modules = {}
        self.objects = {}
        self.current_level = 0; 
        self.selection_mode = False        
        self.levels_availables = []
        self.addRect(QtCore.QRectF(10,10,100,20),QtGui.QPen(),QtGui.QBrush())
        self.setBackgroundBrush(Qt.black)
        self.load_modules()
        
    def load_modules(self):
        mod = HomeHeating.get_instance()
        self.modules[mod.__class__.__name__] = mod
        print "Module %s loaded" % id(mod) 
    # def __mousePressEvent(self,mouseEvent):
#         p = mouseEvent.scenePos()
        
#         if self.is_on_map(self.current_level,p):
#             if self.selection_mode == self.OUTLINE_POINT and self.__cur_op == 'add_area':                
#                 print "llamo a call_update"
#                 self._call_update(mouseEvent)               
            
#             elif self.selection_mode == self.SELECT_MAP_AREA:
                
#                 for it in self.items(p):                    
#                     if HMItem.type(it) == HMItem.MAP_AREA:
#                         if HMItem.select(it) :
#                             HMItem.select(it,False)
#                             it.setBrush(QBrush(Qt.NoBrush))
#                         else:
#                             HMItem.select(it,True)
#                             it.setBrush(QBrush(Qt.Dense4Pattern))
    
                            
#                 self.emit(QtCore.SIGNAL('clickOnMap(point)'),(p))
    
    def remove_by_item(self,item_filter):
        for item in self.items():     
            if HMItem.cmp(item_filter,item):
                self.removeItem(item)          
    
#     def __finish_select_area(self,event):
#         self.__cur_op = ''
#         self.__cur_op_stat = None
#         self.select_mode(self.SELECT_NONE)                       
            
#     def select_mode(self,mode):
#         last_mode = self.selection_mode         
#         self.selection_mode = mode
        
#         if last_mode == self.OUTLINE_POINT :            
#             for it in  self.items():
#                 if HMItem.type(it) == HMItem.OUTLINE_POINT :
#                     self.removeItem(it)
            
#             self.emit(QtCore.SIGNAL('outlineMarked()'))
    
    def set_map(self,pixMap,level=0):
        for item in self.items():            
            if HMItem.level(item) == level:
                self.removeItem(item)           
        
        pixMapItem = QGraphicsPixmapItem(pixMap)
        self.setSceneRect(pixMapItem.boundingRect())
        
        HMItem.name(pixMapItem,self.MAP_ITEM_NAME % level )        
        HMItem.type(pixMapItem, HMItem.MAP)         
        HMItem.level(pixMapItem,level)         
        self.addItem(pixMapItem)
        self.add_level(level)
        self.show_level(level)
    
    def remove_level_items(self,level):
        for it in self.items():
            if HMItem.level(it) == level :
                self.removeItem(it)
    
    def add_level(self,level):
        if level not in self.levels_availables :
            self.levels_availables.append(level)
            self.levels_availables.sort()
            self.emit(SIGNAL('levelAdded(int)'),(level))

    def has_map(self,level):
        its = self.items()
        for it in its:         
            if HMItem.type(it) == HMItem.MAP \
                    and  HMItem.level(it) == level:                  
                return True
        return False
        
            
    def is_on_map(self,level,*args):
        if len(args) == 1: # el argumento es un QPointF
            point = args[0]
        else: #len es 2 (x,y)
            point = QPointF(x,y)
        
        its = self.items(point)
        for it in its:         
            print "%s %d %d" % (HMItem.name(it),HMItem.level(it),level)
            if HMItem.type(it) == HMItem.MAP \
                    and  HMItem.level(it) == level:                  
                return True
        return False
    
    def show_level(self,level,only=False):
        for it in self.items():
            if HMItem.level(it) == -1 : continue
            if HMItem.level(it) == level:
                it.setVisible(True)
                if HMItem.type(it) == HMItem.MAP:
                    self.setSceneRect(it.boundingRect())
            elif only: #seteando only oculta a los que no son del nivel
                it.setVisible(False)

    def hide_level(self,level,only=False):
        for it in self.items():
            if HMItem.level(it) == -1 : continue
            if HMItem.level(it) == level:
                it.setVisible(False)
            elif only : #seteando only oculta a los que no son del nivel
                it.setVisible(True)
        
    def set_current_level(self,level):
        if not isinstance(level,int):
            print "level antes %s " % level
            print repr(level)
            str_level = str(level)
            print "str_level {%s}" % str_level
            match = re.match('^.*(\d+)$',str_level)
            if match:
                str_level = match.groups()[0]
                level = int(str_level)            
            else:
                return
        
        if level in self.levels_availables :            
            self.show_level(level,True)
            self.current_level = level; 
            
            
#     def keyPressEvent(self,event):
#         parent = self.parent()
#         if event.key() == Qt.Key_Escape:            
#             self._call_cancel(event)
#         elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
#             self._call_finish(event)
#         else:
#             event.ignore()
            
    

