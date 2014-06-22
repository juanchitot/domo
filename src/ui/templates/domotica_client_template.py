# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './templates/domotica_client_template.ui'
#
# Created: Sun Jul 17 16:46:49 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Domotica(object):
    def setupUi(self, Domotica):
        Domotica.setObjectName("Domotica")
        Domotica.setWindowModality(QtCore.Qt.ApplicationModal)
        Domotica.setEnabled(True)
        Domotica.resize(878, 685)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Domotica.sizePolicy().hasHeightForWidth())
        Domotica.setSizePolicy(sizePolicy)
        Domotica.setFocusPolicy(QtCore.Qt.StrongFocus)
        Domotica.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.gridLayout = QtGui.QGridLayout(Domotica)
        self.gridLayout.setContentsMargins(30, 30, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.floating_window = FloatingWindow(Domotica)
        self.floating_window.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floating_window.sizePolicy().hasHeightForWidth())
        self.floating_window.setSizePolicy(sizePolicy)
        self.floating_window.setStyleSheet("\n"
"background-color:rgb(216, 255, 238);")
        self.floating_window.setFloating(True)
        self.floating_window.setFeatures(QtGui.QDockWidget.DockWidgetClosable|QtGui.QDockWidget.DockWidgetMovable)
        self.floating_window.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.floating_window.setObjectName("floating_window")
        self.connection_window = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connection_window.sizePolicy().hasHeightForWidth())
        self.connection_window.setSizePolicy(sizePolicy)
        self.connection_window.setObjectName("connection_window")
        self.verticalLayout = QtGui.QVBoxLayout(self.connection_window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.floating_window.setWidget(self.connection_window)
        self.gridLayout.addWidget(self.floating_window, 1, 0, 1, 1)
        self.main_stack = QtGui.QStackedWidget(Domotica)
        self.main_stack.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_stack.setFrameShadow(QtGui.QFrame.Plain)
        self.main_stack.setMidLineWidth(0)
        self.main_stack.setObjectName("main_stack")
        self.user_page_stack = QtGui.QWidget()
        self.user_page_stack.setObjectName("user_page_stack")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.user_page_stack)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.home_map = HomeMap(self.user_page_stack)
        self.home_map.setObjectName("home_map")
        self.horizontalLayout_2.addWidget(self.home_map)
        self.main_stack.addWidget(self.user_page_stack)
        self.admin_page_stack = QtGui.QWidget()
        self.admin_page_stack.setObjectName("admin_page_stack")
        self.horizontalLayout = QtGui.QHBoxLayout(self.admin_page_stack)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.admin_tabs = QtGui.QTabWidget(self.admin_page_stack)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.admin_tabs.sizePolicy().hasHeightForWidth())
        self.admin_tabs.setSizePolicy(sizePolicy)
        self.admin_tabs.setMinimumSize(QtCore.QSize(600, 500))
        font = QtGui.QFont()
        self.admin_tabs.setFont(font)
        self.admin_tabs.setMouseTracking(True)
        self.admin_tabs.setAutoFillBackground(False)
        self.admin_tabs.setStyleSheet("None")
        self.admin_tabs.setTabPosition(QtGui.QTabWidget.North)
        self.admin_tabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.admin_tabs.setElideMode(QtCore.Qt.ElideNone)
        self.admin_tabs.setUsesScrollButtons(True)
        self.admin_tabs.setObjectName("admin_tabs")
        self.tab_admin_home_map = AdminHomeMap()
        self.tab_admin_home_map.setObjectName("tab_admin_home_map")
        self.admin_tabs.addTab(self.tab_admin_home_map, "")
        self.tab_admin_home_lights = AdminHomeLights()
        self.tab_admin_home_lights.setObjectName("tab_admin_home_lights")
        self.admin_tabs.addTab(self.tab_admin_home_lights, "")
        self.tab_admin_home_heating = AdminHomeHeating()
        self.tab_admin_home_heating.setObjectName("tab_admin_home_heating")
        self.admin_tabs.addTab(self.tab_admin_home_heating, "")
        self.tab_admin_light = AdminLight()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_admin_light.sizePolicy().hasHeightForWidth())
        self.tab_admin_light.setSizePolicy(sizePolicy)
        self.tab_admin_light.setObjectName("tab_admin_light")
        self.admin_tabs.addTab(self.tab_admin_light, "")
        self.tab_admin_heating_maps = AdminHeatingMaps()
        self.tab_admin_heating_maps.setObjectName("tab_admin_heating_maps")
        self.admin_tabs.addTab(self.tab_admin_heating_maps, "")
        self.tab_admin_device_mapper = AdminDeviceMapper()
        self.tab_admin_device_mapper.setObjectName("tab_admin_device_mapper")
        self.admin_tabs.addTab(self.tab_admin_device_mapper, "")
        self.tab_ports_status = PortsStatus()
        self.tab_ports_status.setObjectName("tab_ports_status")
        self.admin_tabs.addTab(self.tab_ports_status, "")
        self.tab_manage_cards = ManageCards()
        self.tab_manage_cards.setObjectName("tab_manage_cards")
        self.admin_tabs.addTab(self.tab_manage_cards, "")
        self.horizontalLayout.addWidget(self.admin_tabs)
        self.main_stack.addWidget(self.admin_page_stack)
        self.gridLayout.addWidget(self.main_stack, 0, 0, 1, 1)
        self.actionNombre = QtGui.QAction(Domotica)
        self.actionNombre.setObjectName("actionNombre")

        self.retranslateUi(Domotica)
        self.main_stack.setCurrentIndex(1)
        self.admin_tabs.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(Domotica)

    def retranslateUi(self, Domotica):
        Domotica.setWindowTitle(QtGui.QApplication.translate("Domotica", "Domotica", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_home_map), QtGui.QApplication.translate("Domotica", "Editar Mapa", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_home_lights), QtGui.QApplication.translate("Domotica", "Editar Luces", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_home_heating), QtGui.QApplication.translate("Domotica", "Editar Climatizacio", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_light), QtGui.QApplication.translate("Domotica", "Luces", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_heating_maps), QtGui.QApplication.translate("Domotica", "Maps Climatizacion", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_admin_device_mapper), QtGui.QApplication.translate("Domotica", "Dispositivos", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_ports_status), QtGui.QApplication.translate("Domotica", "Puertos", None, QtGui.QApplication.UnicodeUTF8))
        self.admin_tabs.setTabText(self.admin_tabs.indexOf(self.tab_manage_cards), QtGui.QApplication.translate("Domotica", "Placas", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNombre.setText(QtGui.QApplication.translate("Domotica", "nombre", None, QtGui.QApplication.UnicodeUTF8))

from ui.admin_home_heating import AdminHomeHeating
from ui.home_map import HomeMap
from ui.floating_window import FloatingWindow
from ui.admin_home_map import AdminHomeMap
from ui.admin_home_lights import AdminHomeLights
from ui.ports_status import PortsStatus
from ui.admin_heating_maps import AdminHeatingMaps
from ui.manage_cards import ManageCards
from ui.admin_light import AdminLight
from ui.admin_device_mapper import AdminDeviceMapper
import resources_rc
