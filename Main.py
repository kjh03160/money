# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'framework.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QAbstractTableModel, Qt

from selenium_class import Driver

from baemin_code.baemin_main import baemin_main
from baemin_code.concat_moa import concat
from nowdata_code.now_waiting_main import now_waiting_main
from albam_code.albam_new import albam_pre

from nowdata_code.Now_data import now_data_merge

from statistic_code.albam_statistic import albam_st
from statistic_code.menu import menu_st
from statistic_code.service_statistic import service_st
from statistic_code.deliver_st import deliver_st

from datetime import *

import time
import os
class TestThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.dates = []
        self.main = parent
        self.isRun = False
        self.driver = None

    def run(self):
        self.driver = Driver()
        driver = self.driver
        driver.driver.implicitly_wait(10)
        self.main.start_Crawl.setEnabled(True)

        for i in range(len(self.dates)):
            date = self.dates[i]
            self.threadEvent.emit(date + " 수집 중..")
            # 배민 수집
            try:
                driver = baemin_main(driver, date, i)
                if driver is None:
                    raise Exception
            except PermissionError:
                driver.close()
                self.threadEvent.emit("파일")
                return

            except Exception as err:
                print(err)
                driver.close()

                self.threadEvent.emit("오류")
                self.main.baemin.setText(date + " 부터 다시 시작해주세요.")
                self.main.now_waiting.setText(date + " 부터 다시 시작해주세요.")
                time.sleep(2)

                self.main.start_Crawl.setText("시작")
                return

            # 나우 웨이팅 수집
            driver = now_waiting_main(driver, date, i)
            time.sleep(1)
            self.threadEvent.emit(str(date))
        driver.close()
        time.sleep(2)
        self.main.start_Crawl.setText("시작")
        self.isRun = False
        now_data_merge()
        self.threadEvent.emit("완료")



class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Ui_MainWindow(QMainWindow):

    def setupUi(self, MainWindow):

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1121, 501))

        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)

        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_1)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(230, 20, 841, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.start_Crawl = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.start_Crawl.setObjectName("start_Crawl")
        self.gridLayout.addWidget(self.start_Crawl, 0, 3, 1, 1)
        self.start_date = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.start_date.setFocusPolicy(QtCore.Qt.NoFocus)
        self.start_date.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.start_date.setWrapping(False)
        self.start_date.setFrame(True)
        self.start_date.setAlignment(QtCore.Qt.AlignCenter)
        self.start_date.setReadOnly(False)
        self.start_date.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.start_date.setKeyboardTracking(True)
        self.start_date.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QtCore.QDate(year, month, day))
        self.start_date.setObjectName("start_date")
        self.gridLayout.addWidget(self.start_date, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        # self.label.setFrameShape(QtWidgets.QFrame.Box)
        # self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.end_date = QtWidgets.QDateEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.end_date.setFont(font)
        self.end_date.setFrame(True)
        self.end_date.setAlignment(QtCore.Qt.AlignCenter)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QtCore.QDate(year, month, day))
        self.end_date.setObjectName("end_date")
        self.gridLayout.addWidget(self.end_date, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        # self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        # self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.now_waiting = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.now_waiting.setFont(font)
        self.now_waiting.setText("")
        self.now_waiting.setAlignment(QtCore.Qt.AlignCenter)
        self.now_waiting.setObjectName("now_waiting")
        self.gridLayout.addWidget(self.now_waiting, 2, 2, 1, 1)
        self.baemin = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.baemin.setFont(font)
        self.baemin.setText("")
        self.baemin.setAlignment(QtCore.Qt.AlignCenter)
        self.baemin.setObjectName("baemin")
        self.gridLayout.addWidget(self.baemin, 2, 1, 1, 1)
        self.file_upload = QtWidgets.QPushButton(self.tab_1)
        self.file_upload.setGeometry(QtCore.QRect(830, 320, 261, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.file_upload.setFont(font)
        self.file_upload.setObjectName("file_upload")
        self.upload = QtWidgets.QPushButton(self.tab_1)
        self.upload.setGeometry(QtCore.QRect(970, 370, 121, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.upload.setFont(font)
        self.upload.setObjectName("upload")
        self.label_5 = QtWidgets.QLabel(self.tab_1)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 191, 121))
        self.label_5.setMaximumSize(QtCore.QSize(191, 231))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(self.tab_1)
        self.line.setGeometry(QtCore.QRect(0, 250, 1121, 16))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line2 = QtWidgets.QFrame(self.tab_1)
        self.line2.setGeometry(QtCore.QRect(0, 140, 1121, 10))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.line2.setFont(font)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")

        self.line3 = QtWidgets.QFrame(self.tab_1)
        self.line3.setGeometry(QtCore.QRect(219, 0, 21, 501))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.line3.setFont(font)
        self.line3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setObjectName("line3")


        self.label_6 = QtWidgets.QLabel(self.tab_1)
        self.label_6.setGeometry(QtCore.QRect(20, 260, 191, 231))
        self.label_6.setMaximumSize(QtCore.QSize(191, 231))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.listView = QtWidgets.QListWidget(self.tab_1)
        self.listView.setGeometry(QtCore.QRect(240, 270, 561, 201))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.listView.setFont(font)
        self.listView.setObjectName("listView")
        self.delete_2 = QtWidgets.QPushButton(self.tab_1)
        self.delete_2.setGeometry(QtCore.QRect(830, 370, 121, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.delete_2.setFont(font)
        self.delete_2.setObjectName("delete_2")
        self.label_4 = QtWidgets.QLabel(self.tab_1)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 212, 47))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        # self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.albam_list = QtWidgets.QListWidget(self.tab_1)
        self.albam_list.setGeometry(QtCore.QRect(240, 155, 561, 91))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.albam_list.setFont(font)
        self.albam_list.setObjectName("albam_list")
        self.albam_upload = QtWidgets.QPushButton(self.tab_1)
        self.albam_upload.setGeometry(QtCore.QRect(830, 155, 261, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.albam_upload.setFont(font)
        self.albam_upload.setObjectName("albam_upload")
        self.albam_upload_2 = QtWidgets.QPushButton(self.tab_1)
        self.albam_upload_2.setGeometry(QtCore.QRect(970, 205, 121, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.albam_upload_2.setFont(font)
        self.albam_upload_2.setObjectName("albam_upload_2")
        self.albam_delete = QtWidgets.QPushButton(self.tab_1)
        self.albam_delete.setGeometry(QtCore.QRect(830, 205, 121, 41))
        font = QtGui.QFont()
        font.setFamily("양재인장체M")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.albam_delete.setFont(font)
        self.albam_delete.setObjectName("albam_delete")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 591, 33))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sales_start = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.sales_start.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sales_start.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sales_start.setWrapping(False)
        self.sales_start.setReadOnly(False)
        self.sales_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sales_start.setKeyboardTracking(True)
        self.sales_start.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.sales_start.setCalendarPopup(True)
        self.sales_start.setDate(QtCore.QDate(year, month, day))
        self.sales_start.setObjectName("sales_start")
        self.gridLayout_2.addWidget(self.sales_start, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.sales_statistic = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.sales_statistic.setObjectName("sales_statistic")
        self.gridLayout_2.addWidget(self.sales_statistic, 0, 3, 1, 1)
        self.sales_end = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.sales_end.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sales_end.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sales_end.setWrapping(False)
        self.sales_end.setReadOnly(False)
        self.sales_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sales_end.setKeyboardTracking(True)
        self.sales_end.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.sales_end.setCalendarPopup(True)
        self.sales_end.setDate(QtCore.QDate(year, month, day))
        self.sales_end.setObjectName("sales_end")
        self.gridLayout_2.addWidget(self.sales_end, 0, 2, 1, 1)
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(20, 50, 1101, 421))
        self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")

        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.tableView_10 = QtWidgets.QTableView(self.tab_5)
        self.tableView_10.setGeometry(QtCore.QRect(20, 50, 1091, 421))
        self.tableView_10.setObjectName("tableView_2")
        self.gridLayoutWidget_7 = QtWidgets.QWidget(self.tab_5)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(20, 10, 591, 33))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_3")
        self.order_start = QtWidgets.QDateEdit(self.gridLayoutWidget_7)
        self.order_start.setFocusPolicy(QtCore.Qt.NoFocus)
        self.order_start.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.order_start.setWrapping(False)
        self.order_start.setReadOnly(False)
        self.order_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.order_start.setKeyboardTracking(True)
        self.order_start.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.order_start.setCalendarPopup(True)
        self.order_start.setDate(QtCore.QDate(year, month, day))
        self.order_start.setObjectName("order_start")
        self.gridLayout_7.addWidget(self.order_start, 0, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.gridLayoutWidget_7)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_21, 0, 0, 1, 1)
        self.order_statistic = QtWidgets.QPushButton(self.gridLayoutWidget_7)
        self.order_statistic.setObjectName("order_statistic")
        self.gridLayout_7.addWidget(self.order_statistic, 0, 3, 1, 1)
        self.order_end = QtWidgets.QDateEdit(self.gridLayoutWidget_7)
        self.order_end.setFocusPolicy(QtCore.Qt.NoFocus)
        self.order_end.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.order_end.setWrapping(False)
        self.order_end.setReadOnly(False)
        self.order_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.order_end.setKeyboardTracking(True)
        self.order_end.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.order_end.setCalendarPopup(True)
        self.order_end.setDate(QtCore.QDate(year, month, day))
        self.order_end.setObjectName("order_end")

        self.tableView6 = QtWidgets.QTableView(self.tab_5)
        self.tableView6.setGeometry(QtCore.QRect(20, 50, 1101, 421))
        self.tableView6.setObjectName("tableView")
        self.gridLayout_7.addWidget(self.order_end, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_5, "주문분석")



        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableView_2 = QtWidgets.QTableView(self.tab_3)
        self.tableView_2.setGeometry(QtCore.QRect(20, 50, 1091, 421))
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 591, 33))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.delivery_start = QtWidgets.QDateEdit(self.gridLayoutWidget_3)
        self.delivery_start.setFocusPolicy(QtCore.Qt.NoFocus)
        self.delivery_start.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.delivery_start.setWrapping(False)
        self.delivery_start.setReadOnly(False)
        self.delivery_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.delivery_start.setKeyboardTracking(True)
        self.delivery_start.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.delivery_start.setCalendarPopup(True)
        self.delivery_start.setDate(QtCore.QDate(year, month, day))
        self.delivery_start.setObjectName("delivery_start")
        self.gridLayout_3.addWidget(self.delivery_start, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.delivery_statistic = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.delivery_statistic.setObjectName("delivery_statistic")
        self.gridLayout_3.addWidget(self.delivery_statistic, 0, 3, 1, 1)
        self.deliver_end = QtWidgets.QDateEdit(self.gridLayoutWidget_3)
        self.deliver_end.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deliver_end.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.deliver_end.setWrapping(False)
        self.deliver_end.setReadOnly(False)
        self.deliver_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.deliver_end.setKeyboardTracking(True)
        self.deliver_end.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.deliver_end.setCalendarPopup(True)
        self.deliver_end.setDate(QtCore.QDate(year, month, day))
        self.deliver_end.setObjectName("deliver_end")
        self.gridLayout_3.addWidget(self.deliver_end, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")


        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tableView_3 = QtWidgets.QTableView(self.tab_4)
        self.tableView_3.setGeometry(QtCore.QRect(20, 50, 1091, 421))
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.tab_4)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 10, 591, 33))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labor_start = QtWidgets.QDateEdit(self.gridLayoutWidget_4)
        self.labor_start.setFocusPolicy(QtCore.Qt.NoFocus)
        self.labor_start.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labor_start.setWrapping(False)
        self.labor_start.setReadOnly(False)
        self.labor_start.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.labor_start.setKeyboardTracking(True)
        self.labor_start.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.labor_start.setCalendarPopup(True)
        self.labor_start.setDate(QtCore.QDate(year, month, day))
        self.labor_start.setObjectName("labor_start")
        self.gridLayout_4.addWidget(self.labor_start, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        self.labor_statistic = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.labor_statistic.setObjectName("labor_statistic")
        self.gridLayout_4.addWidget(self.labor_statistic, 0, 3, 1, 1)
        self.labor_end = QtWidgets.QDateEdit(self.gridLayoutWidget_4)
        self.labor_end.setFocusPolicy(QtCore.Qt.NoFocus)
        self.labor_end.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labor_end.setWrapping(False)
        self.labor_end.setReadOnly(False)
        self.labor_end.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.labor_end.setKeyboardTracking(True)
        self.labor_end.setDateTime(QtCore.QDateTime(QtCore.QDate(year, month, day), QtCore.QTime(0, 0, 0)))
        self.labor_end.setCalendarPopup(True)
        self.labor_end.setDate(QtCore.QDate(year, month, day))
        self.labor_end.setObjectName("labor_end")

        # self.tableView0 = QtWidgets.QTableView(self.tab_4)
        # self.tableView0.setGeometry(QtCore.QRect(20, 50, 1101, 421))
        # self.tableView0.setObjectName("tableView")
        self.gridLayout_4.addWidget(self.labor_end, 0, 2, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")







        # self.tab_6 = QtWidgets.QWidget()
        # self.tab_6.setObjectName("tab_6")
        # self.tabWidget.addTab(self.tab_6, "")
        # self.tab_7 = QtWidgets.QWidget()
        # self.tab_7.setObjectName("tab_7")
        # self.tabWidget.addTab(self.tab_7, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # 생각 데이터 완료 버튼 연결해야댐
        self.saenggak_file_list = []
        self.file_upload.clicked.connect(self.saenggak_file)
        self.delete_2.clicked.connect(self.saenggak_removeCurrentItem)
        self.upload.clicked.connect(self.saenggak_fin)


        # 알밤 데이터 완료 버튼 연결해야댐
        self.albam_file_list = []
        self.albam_upload.clicked.connect(self.albam_file)
        self.albam_delete.clicked.connect(self.albam_removeCurrentItem)
        self.albam_upload_2.clicked.connect(self.albam_fin)

        # 통계 연결
        self.sales_statistic.clicked.connect(self.sales_st)
        self.labor_statistic.clicked.connect(self.labor_st)
        self.delivery_statistic.clicked.connect(self.delivery_st)
        self.order_statistic.clicked.connect(self.order_st)


        self.start_Crawl.clicked.connect(self.threadStart)
        # 쓰레드 인스턴스 생성
        self.th = TestThread(self)

        # 쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_Crawl.setText(_translate("MainWindow", "시작"))
        self.label.setText(_translate("MainWindow", "기간"))
        self.label_2.setText(_translate("MainWindow", "배달의민족"))
        self.label_3.setText(_translate("MainWindow", "나우웨이팅"))
        self.file_upload.setText(_translate("MainWindow", "파일 첨부"))
        self.upload.setText(_translate("MainWindow", "완료"))
        self.label_5.setText(_translate("MainWindow", "크롤링"))
        self.label_6.setText(_translate("MainWindow", "생각대로 데이터 첨부"))
        self.delete_2.setText(_translate("MainWindow", "삭제"))
        self.label_4.setText(_translate("MainWindow", "알밤"))
        self.albam_upload.setText(_translate("MainWindow", "파일 첨부"))
        self.albam_upload_2.setText(_translate("MainWindow", "완료"))
        self.albam_delete.setText(_translate("MainWindow", "삭제"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "크롤링"))
        self.label_7.setText(_translate("MainWindow", "검색기간"))
        self.sales_statistic.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "매출분석"))
        self.label_8.setText(_translate("MainWindow", "검색기간"))
        self.delivery_statistic.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "배달분석"))
        self.label_9.setText(_translate("MainWindow", "검색기간"))
        self.labor_statistic.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "인건비"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "주문분석"))
        self.label_21.setText(_translate("MainWindow", "검색기간"))
        self.order_statistic.setText(_translate("MainWindow", "검색"))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "재고"))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "순수익"))

    @pyqtSlot(str)
    def threadEventHandler(self, n):
        if n == "오류":
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "배민 request 거부.\n잠시 후 다시 시도해주세요")

            self.start_Crawl.setText("시작")
            self.th.isRun = False
            self.th.terminate()
        elif n == "파일":
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "csv 파일을 닫아주세요")

            self.start_Crawl.setText("시작")
            self.th.isRun = False
            self.th.terminate()
        elif '수집' in n:
            self.baemin.setText(n)
            self.now_waiting.setText(n)
        elif '-' in n:
            self.baemin.setText(n + " 완료")
            self.now_waiting.setText(n + " 완료")
        else:
            x = QMessageBox()
            self.center()
            x.about(self, "완료", "완료되었습니다!")

    @pyqtSlot()
    def threadStart(self):
        if not self.th.isRun:
            self.th.dates = self.get_dates(self.start_date, self.end_date)
            if self.th.dates is None:
                return
            self.th.isRun = True
            self.start_Crawl.setDisabled(True)
            self.start_Crawl.setText("취소")
            self.th.start()
        else:
            self.th.isRun = False
            x = QMessageBox()
            self.center()
            x.about(self, "경고", "취소하였습니다.")
            self.baemin.setText("취소됨")
            self.now_waiting.setText("취소됨")
            self.th.driver.close()
            self.start_Crawl.setText("시작")

            self.th.terminate()


    def albam_file(self):
        fname = QFileDialog.getOpenFileNames(self)
        for f in fname[0]:
            self.albam_list.addItem(f)
            self.albam_file_list.append(f)

    def albam_fin(self):
        if len(self.albam_file_list) == 0:
            x = QMessageBox()
            self.center()
            x.about(self, "경고", "파일을 첨부해주세요!")
            return
        albam_pre(self.albam_file_list)
        self.albam_list.clear()
        self.albam_file_list.clear()
        x = QMessageBox()
        self.center()
        x.about(self, "완료", "완료되었습니다!")

    def albam_removeCurrentItem(self) :
        #ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다.
        removeItemRow = self.albam_list.currentRow()
        self.albam_list.takeItem(removeItemRow)
        self.albam_file_list.pop(removeItemRow)


    def saenggak_file(self):
        fname = QFileDialog.getOpenFileNames(self)
        for f in fname[0]:
            self.listView.addItem(f)
            self.saenggak_file_list.append(f)

    def saenggak_removeCurrentItem(self) :
        #ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다.
        removeItemRow = self.listView.currentRow()
        self.listView.takeItem(removeItemRow)
        self.saenggak_file_list.pop(removeItemRow)

    def saenggak_fin(self):
        if len(self.saenggak_file_list) == 0:
            x = QMessageBox()
            self.center()
            x.about(self, "경고", "파일을 첨부해주세요!")
            return
        bool = concat(self.saenggak_file_list)
        self.saenggak_file_list.clear()

        self.listView.clear()

        x = QMessageBox()
        self.center()

        if bool:
            x.about(self, "완료", "매칭 안된 데이터가 존재합니다.")
            cur = os.getcwd()
            os.chdir(cur)
            os.startfile(".\\data\\baemin\\not_matched.csv")
            os.startfile(".\\data\\baemin\\Accumulated_data.csv")
        else:
            x.about(self, "완료", "완료되었습니다!")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sales_st(self):
        dates = self.get_dates(self.sales_start, self.sales_end)
        if dates is None:
            return
        df = menu_st(dates)
        if df is False:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "데이터가 없습니다.")
            return
        model = pandasModel(df)
        self.tableView.setModel(model)

    def order_st(self):
        dates = self.get_dates(self.order_start, self.order_end)
        if dates is None:
            return
        df = service_st(dates)
        if df is False:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "데이터가 없습니다.")
            return

        model = pandasModel(df)
        self.tableView6.setModel(model)

    def delivery_st(self):
        dates = self.get_dates(self.delivery_start, self.deliver_end)
        if dates is None:
            return

        df = deliver_st(dates)
        if df is False:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "데이터가 없습니다.")
            return
        model = pandasModel(df)
        self.tableView_2.setModel(model)

    def labor_st(self):

        dates = self.get_dates(self.labor_start, self.labor_end)
        if dates is None:
            return
        df = albam_st(dates)
        if df is False:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "데이터가 없습니다.")
            return
        model = pandasModel(df)
        self.tableView_3.setModel(model)

    def get_dates(self, start, end):
        start_date = list(map(int, start.text().split('-')))
        end_date = list(map(int, end.text().split('-')))
        start_date = datetime(start_date[0], start_date[1], start_date[2])
        end_date = datetime(end_date[0], end_date[1], end_date[2])
        date = []
        if start_date > end_date:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "날짜를 확인해주세요")
            return
        while start_date <= end_date:
            date.append(start_date.strftime('%Y-%m-%d'))
            start_date = start_date + timedelta(days=1)
        return date

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    input()


