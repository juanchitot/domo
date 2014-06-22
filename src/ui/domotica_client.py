import sys

from PyQt4 import QtCore, \
    QtGui

from PyQt4.QtCore import QVariant, \
    Qt, \
    QString ,\
    QEvent, \
    SIGNAL, \
    QLocale, \
    QCoreApplication as QCA, \
    QCoreApplication , \
    QObject ,\
    SLOT


from PyQt4.QtGui import QVBoxLayout, \
    QKeySequence, \
    QCursor, \
    QApplication, \
    QAction, \
    QMenuBar, \
    QMenu

from ui.templates.domotica_client_template import Ui_Domotica

from ui.client_core import ClientCore

class DomoticaClient(QtGui.QWidget,Ui_Domotica):
    
    MAIN_WINDOW = None
    
    USER_STACK_INDEX = 0;
    ADMIN_STACK_INDEX = 1;
    
    def __init__(self,parent):
        QtGui.QWidget.__init__(self,parent)
        self.main_window = parent
        self.menu_bar = parent.menuBar()
        self.setupUi(self)        
        
        self.floating_window.setWidget(self.floating_window.dockWidgetContents)                
        
        self.client_core = ClientCore.get_instance()
        
        self.build_menu()
        self.setup_connections()                
#         self.setLocale(QLocale(QLocale.English))
            
    def build_menu(self):
        menu = QMenu( QCA.translate('DomoticaClient' ,'Menu'),
                      self)      
        
        if self.main_stack.currentIndex() == self.ADMIN_STACK_INDEX:
            action = QAction(QCA.translate('DomoticaClient' ,'Modo Usuario'),menu)
            QtCore.QObject.connect(action,SIGNAL("triggered()"),self.goto_user_mode)
            menu.addAction(action)
            
        else:                
            self.unpublish_menu(['DOMOTICA_MENU'],'leave')
            action = QAction(QCA.translate('DomoticaClient' ,'Modo Administrador'),menu)
            QtCore.QObject.connect(action,SIGNAL("triggered()"),self.goto_admin_mode)
            menu.addAction(action)
            
        action = QAction(QCA.translate('DomoticaClient' ,'Desconectar'),menu)
        menu.addAction(action)
        
        action = QAction(QCA.translate('DomoticaClient' ,'Cerrar'),menu)
        QObject.connect(action,SIGNAL("triggered()"),QCA.exit)
        menu.addAction(action)
        
        self.publish_menu('DOMOTICA_MENU',menu)
            
        
    def publish_menu(self,menu_key, menu):
        act_exists = None
        for action in self.menu_bar.actions():                        
            key = str(action.property('menu_key').toString())
            if key == menu_key:
                act_exists = action
                
        if act_exists :
            act_exists.setMenu(menu)
        else:
            action = self.menu_bar.addMenu(menu)
            action.setProperty('menu_key', menu_key)
        
    #en method paso 'remove' o 'leave' para que las acciones pasadas sean
    #las que se borran o las que se quedan
    def unpublish_menu(self,act_keys,method='remove'):

        for action in self.menu_bar.actions():
            key = str(action.property('menu_key').toString())            
            if method == 'remove':                
                if key and key in act_keys:                
                    self.menu_bar.removeAction(action)
            else:
                if key not in act_keys:                                    
                    self.menu_bar.removeAction(action)
    
    def goto_user_mode(self):
        self.main_stack.setCurrentIndex(self.USER_STACK_INDEX) 
        self.build_menu()
    
    def goto_admin_mode(self):
        self.main_stack.setCurrentIndex(self.ADMIN_STACK_INDEX) 
        self.build_menu()
        self.admin_tabs.emit(SIGNAL("currentChanged(int)"),(0))
    
    def setup_connections(self):
        
        for i in range(self.admin_tabs.count()):
            # QtCore.QObject.connect(self.admin_tabs.widget(i),
            #                        SIGNAL("removeMenu(title)"),
            #                        self.unpublish_menu)

            # QtCore.QObject.connect(self.admin_tabs.widget(i),
            #                        SIGNAL("menuChanged(title,menu)"),
            #                        self.publish_menu)
            #
            QtCore.QObject.connect(self.admin_tabs,
                                   SIGNAL("currentChanged(int)"),
                                   self.admin_tabs.widget(i).tab_changed)
            
        
    def closeEvent(self,event):
        self.client_core.save_configuration()
        QCoreApplication.quit()
        
