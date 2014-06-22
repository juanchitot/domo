import re
from PyQt4.QtGui import QFrame, QTableWidgetItem

from ui.templates.analogic_card_status_template import Ui_Frame

class AnalogicCardStatus(QFrame, Ui_Frame):
    
    def __init__(self,widget,card_id):        
        QFrame.__init__(self,widget)
        self.setupUi(self)
        self.card_id = card_id
        self.table_name.setText( "Analogic Card (%s)" % card_id )
        self.client_core = widget.client_core
        self.initialize_table()
    
    def update_ports(self):
        g = re.match( "([A-Z]+[a-z]+\_[0-9]+)\_([0-9]+)", self.card_id )
        
        pat_in_ports = re.compile( "%s\_I\_%s\_([0-9]+)" % g.groups() )
        
        for port_id, port in self.client_core.in_ports.items():
            m = pat_in_ports.match(port_id) 
            if m :                 
                port_number =  int(m.groups()[0])                                
                self.ports_table.setItem(port_number,
                                         0,
                                         QTableWidgetItem("%d" % port.value ))
                
    def initialize_table(self):
        for i in range(9):
            self.ports_table.setItem( i, 0, QTableWidgetItem(""))
                
