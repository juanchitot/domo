# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './domotica.ui'
#
# Created: Wed Jul  1 17:32:59 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Domotica(object):
    def setupUi(self, Domotica):
        Domotica.setObjectName("Domotica")
        Domotica.setEnabled(True)
        Domotica.resize(812, 756)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Domotica.sizePolicy().hasHeightForWidth())
        Domotica.setSizePolicy(sizePolicy)
        Domotica.setStyleSheet("background-color:rgb(222, 255, 185);")
        self.verticalLayoutWidget_2 = QtGui.QWidget(Domotica)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 50, 761, 691))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.admin_tabs = QtGui.QTabWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.admin_tabs.sizePolicy().hasHeightForWidth())
        self.admin_tabs.setSizePolicy(sizePolicy)
        self.admin_tabs.setMinimumSize(QtCore.QSize(600, 500))
        self.admin_tabs.setObjectName("admin_tabs")
        self.tab_map_ligth = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_map_ligth.sizePolicy().hasHeightForWidth())
        self.tab_map_ligth.setSizePolicy(sizePolicy)
        self.tab_map_ligth.setObjectName("tab_map_ligth")
        self.verticalLayoutWidget = QtGui.QWidget(self.tab_map_ligth)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, -40, 802, 751))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.admin_ligth_frame = AdminLightFrame(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.admin_ligth_frame.sizePolicy().hasHeightForWidth())
        self.admin_ligth_frame.setSizePolicy(sizePolicy)
        self.admin_ligth_frame.setMinimumSize(QtCore.QSize(800, 600))
        self.admin_ligth_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.admin_ligth_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.admin_ligth_frame.setObjectName("admin_ligth_frame")
        self.verticalLayout.addWidget(self.admin_ligth_frame)
        self.admin_tabs.addTab(self.tab_map_ligth, "")
        self.tab_ports_status = QtGui.QWidget()
        self.tab_ports_status.setObjectName("tab_ports_status")
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.tab_ports_status)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 901, 761))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ports_status_frame = PortsStatusFrame(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ports_status_frame.sizePolicy().hasHeightForWidth())
        self.ports_status_frame.setSizePolicy(sizePolicy)
        self.ports_status_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ports_status_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.ports_status_frame.setObjectName("ports_status_frame")
        self.verticalLayout_3.addWidget(self.ports_status_frame)
        self.admin_tabs.addTab(self.tab_ports_status, "")
        self.verticalLayout_2.addWidget(self.admin_tabs)
        self.pushButton = QtGui.QPushButton(Domotica)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 75, 25))
        self.pushButton.setObjectName("pushButton")
        self.actionNombre = QtGui.QAction(Domotica)
        self.actionNombre.setObjectName("actionNombre")

        self.retranslateUi(Domotica)
        self.admin_tabs.setCurrentIndex(1)
        QtCore.QObject.connect(self.admin_tabs, QtCore.SIGNAL("currentChanged(int)"), self.ports_status_frame.tab_change)
        QtCore.QMetaObject.connectSlotsByName(Domotica)

    def retranslateUi(self, Domotica):
        Domotica.setWindowTitle(QtGui.QApplication.translate("Domotica", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_map_ligth), QtGui.QApplication.translate("Domotica", "Luces", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_ports_status), QtGui.QApplication.translate("Domotica", "Puertos", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Domotica", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNombre.setText(QtGui.QApplication.translate("Domotica", "nombre", None, QtGui.QApplication.UnicodeUTF8))

from ui.ports_status_frame import PortsStatusFrame
from ui.admin_light_frame import AdminLightFrame
