import re
from PyQt4.QtGui import QFrame, QTableWidgetItem
from PyQt4.QtCore import QSize
from ui.templates.digital_card_status_template import Ui_Frame

class DigitalCardStatus(QFrame,Ui_Frame):
    def __init__(self,widget,card_id):        
        QFrame.__init__(self,widget)
        self.setupUi(self)
        self.card_id = card_id
        self.table_name.setText( "Digital Card (%s)" % card_id )
        self.client_core = widget.client_core
        self.initialize_table()
    
    def sizeHint(self):
        return QSize(self.width(),self.height())
    
    def initialize_table(self):
        for i in range(14):
            self.ports_table.setItem(i,0,QTableWidgetItem("0"))
            self.ports_table.setItem(i,1,QTableWidgetItem("0"))
        
    def update_ports(self):
        g = re.match( "([A-Z]+[a-z]+\_[0-9]+)\_([0-9]+)", self.card_id )
        
        pat_in_ports = re.compile( "%s\_I\_%s\_([0-9]+)" % g.groups() )
        for port_id, port in self.client_core.in_ports.items():
            m = pat_in_ports.match(port_id) 
            if m :                 
                port_number =  int(m.groups()[0])                
                t_it = self.ports_table.item(port_number,0)
                t_it.setText("%d" % port.value )
        
        pat_out_ports = re.compile( "%s\_O\_%s\_([0-9]+)" % g.groups() )
        for port_id, port in self.client_core.out_ports.items():           
            m = pat_out_ports.match(port_id)
            if m :   # es un out_port
                port_number =  int(m.groups()[0])
                t_it = self.ports_table.item(port_number,1)
                t_it.setText("%d" % port.value )
                
    def change_port(self,row,column):
        if column == 1:
            t_it = self.ports_table.item(row,column)
            it_value = int( t_it.text() )            
            it_value = (it_value+1)%2
            t_it.setText("%d" % it_value )        
            
            port_name = self.build_port_name(row,column)
            
            self.client_core.out_ports[port_name].set_value(it_value)
            
            self.client_core.set_ports([port_name])

    def build_port_name(self,row,column):
        g = re.match('(Bus)\_(\d)\_(\d{2})',self.card_id).groups()
        if column == 0:
            ret = "%s_%s_I_%s" % g
            ret += "_%02d" % row            
        else:
            ret = "%s_%s_O_%s" % g
            ret += "_%02d" % row            
        return ret
