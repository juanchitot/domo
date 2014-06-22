#!/usr/bin/python  -d

import sys


from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import QApplication, \
    QStyleFactory, \
    QWidget

from ui.templates.dom_tree import Ui_Form

app = QtGui.QApplication(sys.argv)

QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

class Test(QWidget,Ui_Form):
    
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setupUi(self)

form = Test()

form.webView.setHtml('''<html>
<body style="background-color:blue;">
<table>
<tr>
  <td>
    casa
  </td>
  <td>
    <input type="button" onclick="javascript:alert('hola');" value="Click" />
  </td>
</tr>
</table>
</body>
</html>
''')

main_window = QtGui.QMainWindow()
main_window.setCentralWidget( form )
main_window.show()

app.exec_()


