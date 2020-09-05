# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'framework.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from main import main
from PyQt5.QtCore import *
import sys
import datetime


class TestThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False

    def run(self):
        while self.isRun:
            print('쓰레드 : ' + str(self.n))

            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)

            self.n += 1
            self.sleep(1)

class Ui_MainWindow(QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1121, 501))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_1)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(220, 20, 871, 191))
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
        self.start_date.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 1), QtCore.QTime(0, 0, 0)))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QtCore.QDate(2020, 9, 1))
        self.start_date.setObjectName("start_date")
        self.gridLayout.addWidget(self.start_date, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.end_date = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.end_date.setFrame(True)
        self.end_date.setAlignment(QtCore.Qt.AlignCenter)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QtCore.QDate(2020, 9, 1))
        self.end_date.setObjectName("end_date")
        self.gridLayout.addWidget(self.end_date, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.baemin = QtWidgets.QLabel(self.gridLayoutWidget)
        self.baemin.setAlignment(QtCore.Qt.AlignCenter)
        self.baemin.setObjectName("baemin")
        self.gridLayout.addWidget(self.baemin, 1, 1, 1, 1)
        self.now_waiting = QtWidgets.QLabel(self.gridLayoutWidget)
        self.now_waiting.setAlignment(QtCore.Qt.AlignCenter)
        self.now_waiting.setObjectName("now_waiting")
        self.gridLayout.addWidget(self.now_waiting, 2, 1, 1, 1)
        self.albam = QtWidgets.QLabel(self.gridLayoutWidget)
        self.albam.setAlignment(QtCore.Qt.AlignCenter)
        self.albam.setObjectName("albam")
        self.gridLayout.addWidget(self.albam, 3, 1, 1, 1)


        self.file_upload = QtWidgets.QPushButton(self.tab_1)
        self.file_upload.setGeometry(QtCore.QRect(810, 290, 261, 41))
        self.file_upload.setObjectName("file_upload")


        self.upload = QtWidgets.QPushButton(self.tab_1)
        self.upload.setGeometry(QtCore.QRect(990, 370, 61, 41))
        self.upload.setObjectName("upload")
        self.label_5 = QtWidgets.QLabel(self.tab_1)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 191, 231))
        self.label_5.setMaximumSize(QtCore.QSize(191, 231))
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(self.tab_1)
        self.line.setGeometry(QtCore.QRect(0, 250, 1121, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_6 = QtWidgets.QLabel(self.tab_1)
        self.label_6.setGeometry(QtCore.QRect(30, 270, 191, 231))
        self.label_6.setMaximumSize(QtCore.QSize(191, 231))
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.listView = QtWidgets.QListWidget(self.tab_1)
        self.listView.setGeometry(QtCore.QRect(230, 270, 561, 201))
        self.listView.setObjectName("listView")
        self.delete_2 = QtWidgets.QPushButton(self.tab_1)
        self.delete_2.setGeometry(QtCore.QRect(810, 370, 121, 41))
        self.delete_2.setObjectName("delete_2")


        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 401, 33))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dateEdit_3 = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.dateEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dateEdit_3.setWrapping(False)
        self.dateEdit_3.setReadOnly(False)
        self.dateEdit_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dateEdit_3.setKeyboardTracking(True)
        self.dateEdit_3.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_3.setCalendarPopup(True)
        self.dateEdit_3.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_3.setObjectName("dateEdit_3")
        self.gridLayout_2.addWidget(self.dateEdit_3, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 3, 1, 1)
        self.dateEdit_4 = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.dateEdit_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_4.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dateEdit_4.setWrapping(False)
        self.dateEdit_4.setReadOnly(False)
        self.dateEdit_4.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dateEdit_4.setKeyboardTracking(True)
        self.dateEdit_4.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_4.setCalendarPopup(True)
        self.dateEdit_4.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_4.setObjectName("dateEdit_4")
        self.gridLayout_2.addWidget(self.dateEdit_4, 0, 2, 1, 1)
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(20, 70, 1101, 651))
        self.tableView.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 401, 33))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.dateEdit_5 = QtWidgets.QDateEdit(self.gridLayoutWidget_3)
        self.dateEdit_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_5.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dateEdit_5.setWrapping(False)
        self.dateEdit_5.setReadOnly(False)
        self.dateEdit_5.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dateEdit_5.setKeyboardTracking(True)
        self.dateEdit_5.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_5.setCalendarPopup(True)
        self.dateEdit_5.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_5.setObjectName("dateEdit_5")
        self.gridLayout_3.addWidget(self.dateEdit_5, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.pushButton_5, 0, 3, 1, 1)
        self.dateEdit_6 = QtWidgets.QDateEdit(self.gridLayoutWidget_3)
        self.dateEdit_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_6.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dateEdit_6.setWrapping(False)
        self.dateEdit_6.setReadOnly(False)
        self.dateEdit_6.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dateEdit_6.setKeyboardTracking(True)
        self.dateEdit_6.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 9, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit_6.setCalendarPopup(True)
        self.dateEdit_6.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_6.setObjectName("dateEdit_6")
        self.gridLayout_3.addWidget(self.dateEdit_6, 0, 2, 1, 1)
        self.tableView_2 = QtWidgets.QTableView(self.tab_3)
        self.tableView_2.setGeometry(QtCore.QRect(20, 70, 1101, 651))
        self.tableView_2.setObjectName("tableView_2")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.tab_4)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 10, 401, 33))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_5.addWidget(self.pushButton_7, 0, 3, 1, 1)
        self.dateEdit_9 = QtWidgets.QDateEdit(self.gridLayoutWidget_4)
        self.dateEdit_9.setCalendarPopup(True)
        self.dateEdit_9.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_9.setObjectName("dateEdit_9")
        self.gridLayout_5.addWidget(self.dateEdit_9, 0, 2, 1, 1)
        self.dateEdit_10 = QtWidgets.QDateEdit(self.gridLayoutWidget_4)
        self.dateEdit_10.setCalendarPopup(True)
        self.dateEdit_10.setDate(QtCore.QDate(2020, 9, 1))
        self.dateEdit_10.setObjectName("dateEdit_10")
        self.gridLayout_5.addWidget(self.dateEdit_10, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tabWidget.addTab(self.tab_7, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.file_list = []
        self.file_upload.clicked.connect(self.file)
        self.delete_2.clicked.connect(self.removeCurrentItem)
        self.start_Crawl.clicked.connect(self.crawling)

        # https://www.da-hae.kr/pyqt5-qthread-%EC%82%AC%EC%9A%A9%EB%B2%95/
        # https://m.blog.naver.com/PostView.nhn?blogId=townpharm&logNo=220959370280&proxyReferer=https:%2F%2Fwww.google.com%2F
        # 쓰레드 인스턴스 생성
        self.th = TestThread(self)

        # 쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_Crawl.setText(_translate("MainWindow", "검색"))
        self.label_2.setText(_translate("MainWindow", "배달의민족"))
        self.label.setText(_translate("MainWindow", "검색기간"))
        self.label_3.setText(_translate("MainWindow", "나우웨이팅"))
        self.label_4.setText(_translate("MainWindow", "알밤"))
        self.file_upload.setText(_translate("MainWindow", "파일 첨부"))
        self.upload.setText(_translate("MainWindow", "완료"))
        self.label_5.setText(_translate("MainWindow", "크롤링"))
        self.label_6.setText(_translate("MainWindow", "생각대로 데이터 첨부"))
        self.delete_2.setText(_translate("MainWindow", "삭제"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "크롤링"))
        self.label_7.setText(_translate("MainWindow", "검색기간"))
        self.pushButton_4.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "매출분석"))
        self.label_8.setText(_translate("MainWindow", "검색기간"))
        self.pushButton_5.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "배달분석"))
        self.label_10.setText(_translate("MainWindow", "검색기간"))
        self.pushButton_7.setText(_translate("MainWindow", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "인건비"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "매입"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "재고"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "순수익"))

    def file(self):
        fname = QFileDialog.getOpenFileNames(self)
        print(fname)
        for f in fname[0]:
            # x = QtWidgets.QLabel(self.listView)
            self.listView.addItem(f)
            self.file_list.append(f)
        pass
    def removeCurrentItem(self) :
        #ListWidget에서 현재 선택한 항목을 삭제할 때는 선택한 항목의 줄을 반환한 후, takeItem함수를 이용해 삭제합니다.
        removeItemRow = self.listView.currentRow()
        self.listView.takeItem(removeItemRow)
        self.file_list.pop(removeItemRow)


    def crawling(self):
        start_date = list(map(int, self.start_date.text().split('-')))
        end_date = list(map(int, self.end_date.text().split('-')))
        start_date = datetime.datetime(start_date[0], start_date[1], start_date[2])
        end_date = datetime.datetime(end_date[0], end_date[1], end_date[2])
        date = []
        if start_date > end_date:
            x = QMessageBox()
            self.center()
            x.about(self, "오류", "날짜를 확인해주세요")
            return
        while start_date <= end_date:
            date.append(start_date.strftime('%Y-%m-%d'))
            start_date = start_date + datetime.timedelta(days=1)
        return self.start_c(date)

    def start_c(self, date):
        main(self, date)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

