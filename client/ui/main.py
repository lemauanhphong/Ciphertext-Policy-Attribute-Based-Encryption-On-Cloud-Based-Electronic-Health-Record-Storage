# Form implementation generated from reading ui file './ui/main.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1028, 727)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cb_table = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cb_table.setObjectName("cb_table")
        self.cb_table.addItem("")
        self.cb_table.addItem("")
        self.cb_table.addItem("")
        self.cb_table.addItem("")
        self.gridLayout_2.addWidget(self.cb_table, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.le_address = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_address.setObjectName("le_address")
        self.gridLayout_2.addWidget(self.le_address, 3, 1, 1, 1)
        self.lbl_address = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_address.setObjectName("lbl_address")
        self.gridLayout_2.addWidget(self.lbl_address, 3, 0, 1, 1)
        self.le_name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_name.setObjectName("le_name")
        self.gridLayout_2.addWidget(self.le_name, 1, 1, 1, 1)
        self.le_description = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_description.setObjectName("le_description")
        self.gridLayout_2.addWidget(self.le_description, 4, 1, 1, 1)
        self.lbl_description = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_description.setObjectName("lbl_description")
        self.gridLayout_2.addWidget(self.lbl_description, 4, 0, 1, 1)
        self.lbl_uid = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_uid.setObjectName("lbl_uid")
        self.gridLayout_2.addWidget(self.lbl_uid, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_uid = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_uid.setObjectName("le_uid")
        self.horizontalLayout.addWidget(self.le_uid)
        self.lbl_date_of_birth = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_date_of_birth.setObjectName("lbl_date_of_birth")
        self.horizontalLayout.addWidget(self.lbl_date_of_birth)
        self.le_date_of_birth = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_date_of_birth.setObjectName("le_date_of_birth")
        self.horizontalLayout.addWidget(self.le_date_of_birth)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_0 = QtWidgets.QWidget()
        self.tab_0.setObjectName("tab_0")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_found_items = QtWidgets.QTableWidget(parent=self.tab_0)
        self.tb_found_items.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tb_found_items.setObjectName("tb_found_items")
        self.tb_found_items.setColumnCount(5)
        self.tb_found_items.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tb_found_items.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_found_items.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_found_items.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_found_items.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tb_found_items.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tb_found_items)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_search = QtWidgets.QPushButton(parent=self.tab_0)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout_5.addWidget(self.btn_search)
        self.btn_download = QtWidgets.QPushButton(parent=self.tab_0)
        self.btn_download.setObjectName("btn_download")
        self.horizontalLayout_5.addWidget(self.btn_download)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_0, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.tab_1)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pte_policy = QtWidgets.QPlainTextEdit(parent=self.tab_1)
        self.pte_policy.setObjectName("pte_policy")
        self.verticalLayout_2.addWidget(self.pte_policy)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(parent=self.tab_1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.le_file_name = QtWidgets.QLineEdit(parent=self.tab_1)
        self.le_file_name.setObjectName("le_file_name")
        self.horizontalLayout_3.addWidget(self.le_file_name)
        self.btn_browse = QtWidgets.QPushButton(parent=self.tab_1)
        self.btn_browse.setAutoFillBackground(False)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout_3.addWidget(self.btn_browse)
        self.btn_upload = QtWidgets.QPushButton(parent=self.tab_1)
        self.btn_upload.setObjectName("btn_upload")
        self.horizontalLayout_3.addWidget(self.btn_upload)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_1, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1028, 24))
        self.menubar.setObjectName("menubar")
        self.menuSession = QtWidgets.QMenu(parent=self.menubar)
        self.menuSession.setObjectName("menuSession")
        main_window.setMenuBar(self.menubar)
        self.act_login = QtGui.QAction(parent=main_window)
        self.act_login.setObjectName("act_login")
        self.act_logout = QtGui.QAction(parent=main_window)
        self.act_logout.setObjectName("act_logout")
        self.act_quit = QtGui.QAction(parent=main_window)
        self.act_quit.setObjectName("act_quit")
        self.act_change_password = QtGui.QAction(parent=main_window)
        self.act_change_password.setObjectName("act_change_password")
        self.menuSession.addAction(self.act_change_password)
        self.menuSession.addAction(self.act_logout)
        self.menuSession.addAction(self.act_quit)
        self.menubar.addAction(self.menuSession.menuAction())

        self.retranslateUi(main_window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "ABE Client"))
        self.cb_table.setItemText(0, _translate("main_window", "person_profiles"))
        self.cb_table.setItemText(1, _translate("main_window", "health_records"))
        self.cb_table.setItemText(2, _translate("main_window", "researches"))
        self.cb_table.setItemText(3, _translate("main_window", "financials"))
        self.label_4.setText(_translate("main_window", "Category"))
        self.label_6.setText(_translate("main_window", "Name"))
        self.lbl_address.setText(_translate("main_window", "Address"))
        self.lbl_description.setText(_translate("main_window", "Description"))
        self.lbl_uid.setText(_translate("main_window", "User ID"))
        self.lbl_date_of_birth.setText(_translate("main_window", "Date of birth"))
        item = self.tb_found_items.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "ID"))
        item = self.tb_found_items.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "Name"))
        item = self.tb_found_items.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "File name"))
        item = self.tb_found_items.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "Description"))
        item = self.tb_found_items.horizontalHeaderItem(4)
        item.setText(_translate("main_window", "Last modified"))
        self.btn_search.setText(_translate("main_window", "Search"))
        self.btn_download.setText(_translate("main_window", "Download selected items"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("main_window", "Download from Cloud"))
        self.label.setText(_translate("main_window", "Encryption Policy"))
        self.label_5.setText(_translate("main_window", "File to upload"))
        self.btn_browse.setText(_translate("main_window", "Browse"))
        self.btn_upload.setText(_translate("main_window", "Upload"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("main_window", "Upload to Cloud"))
        self.menuSession.setTitle(_translate("main_window", "Session"))
        self.act_login.setText(_translate("main_window", "Login"))
        self.act_logout.setText(_translate("main_window", "Logout"))
        self.act_quit.setText(_translate("main_window", "Quit"))
        self.act_change_password.setText(_translate("main_window", "Change password"))
