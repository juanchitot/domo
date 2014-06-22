from PyQt4.QtCore import SIGNAL

from PyQt4.QtCore import QObject

class AdminTab(QObject):
    
    view_initialized = False
    initialized = False
    
    def show_tab(self):
        if not self.view_initialized:
            self.initialize_view()

    def initialize_view(self):
        self.view_initialized = True
        
    def tab_changed(self):
        parent = self.parentWidget()
        if self == parent.currentWidget() :
            menu = self.build_menu()
            self.emit(SIGNAL("menuChanged(title,menu)"),self.MENU_KEY,menu)                
            self.show_tab()
            if not self.initialized:
                self.initialize()
                self.initialized = True
        else:
            self.emit(SIGNAL("removeMenu(title)"),self.MENU_KEY)                
                
