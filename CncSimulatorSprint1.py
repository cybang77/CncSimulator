import os, sys, time, csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from kafka import KafkaProducer
import threading

class Ui_CNC_Simulator(object):
    def __init__(self):
        # self.history = os.path.isfile('./tmp')
        self.data = None
        self.flag = False
        self.makeAnomal = False
        self.start = 0
        self.end = 0
        self.logs = ''
        self.interval = 0.05
        self.producer = KafkaProducer(bootstrap_servers=['9.8.100.152:9092'])
        self.topic = 'cnc_test'
        self.kafkaSendThread = threading.Thread(target=self.SendData, name="kafkaSendThread", args=())
        self.kafkaSendThread.start()
        self.anomalyLog = ''

    def setupUi(self, CNC_Simulator):
        CNC_Simulator.setObjectName("CNC_Simulator")
        CNC_Simulator.resize(1256, 603)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/Users/1027a/Downloads/tmp/logo2.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CNC_Simulator.setWindowIcon(icon)
        CNC_Simulator.setStyleSheet("background-color: #0a1a33;")
        self.centralwidget = QtWidgets.QWidget(CNC_Simulator)
        self.centralwidget.setObjectName("centralwidget")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(15, 7, 1231, 31))
        self.header.setStyleSheet("Color: white; font: 75 20pt \"URW Gothic L\"; font-weight: 700;")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")

        self.error = QtWidgets.QMessageBox()
        self.error.setWindowTitle("ERROR!")
        self.error.setIcon(QtWidgets.QMessageBox.Critical)

        self.info = QtWidgets.QMessageBox()
        self.info.setWindowTitle("INFOMATION")
        self.info.setIcon(QtWidgets.QMessageBox.Critical)

        self.module1 = QtWidgets.QLabel(self.centralwidget)
        self.module1.setGeometry(QtCore.QRect(13, 47, 588, 308))
        self.module1.setStyleSheet("background-color: #092c4c; border-radius: 10px;")
        self.module1.setObjectName("module1")
        self.filePath = QtWidgets.QLabel(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(23, 60, 488, 31))
        self.filePath.setStyleSheet("Color: white; border: 1.5px solid gray; background-color: #3a475a; font: 75 10pt \"URW Gothic L\"; border-radius: 5px")
        self.filePath.setObjectName("filePath")
        self.browsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browsBtn.setGeometry(QtCore.QRect(515, 59, 79, 31))
        self.browsBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browsBtn.setStyleSheet("Color: white; background-color: #0F79DB; font-size: 11pt; font-weight: 600; border-radius: 5px;")
        self.browsBtn.setObjectName("browsBtn")
        self.fileInfo = QtWidgets.QLabel(self.centralwidget)
        self.fileInfo.setAlignment(QtCore.Qt.AlignTop)
        self.fileInfo.setGeometry(QtCore.QRect(23, 97, 570, 252))
        self.fileInfo.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.fileInfo.setStyleSheet("Color: white; background-color: #3a475a; font: 75 10pt \"URW Gothic L\"; border-radius: 5px; padding: 3px;")
        self.fileInfo.setObjectName("fileInfo")
        self.module2 = QtWidgets.QLabel(self.centralwidget)
        self.module2.setGeometry(QtCore.QRect(11, 474, 590, 112))
        self.module2.setStyleSheet("background-color: #092c4c; border-radius: 10px;")
        self.module2.setObjectName("module2")
        end = QtWidgets.QLabel(self.centralwidget)
        end.setGeometry(QtCore.QRect(218, 482, 182, 17))
        end.setStyleSheet("Color: white; background-color: #092c4c; font: 75 13pt \"URW Gothic L\";")
        end.setAlignment(QtCore.Qt.AlignCenter)
        end.setObjectName("end")
        end.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "end index"))
        self.endIndex = QtWidgets.QLineEdit(self.centralwidget)
        self.endIndex.setGeometry(QtCore.QRect(217, 506, 186, 25))
        self.endIndex.setValidator(QtGui.QIntValidator(0,999999999))
        self.endIndex.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")
        self.endIndex.setObjectName("endIndex")
        self.tilde = QtWidgets.QLabel(self.centralwidget)
        self.tilde.setGeometry(QtCore.QRect(203, 484, 15, 16))
        self.tilde.setStyleSheet("Color: white; background-color: #092c4c; font-size: 20pt;")
        self.tilde.setObjectName("tilde")
        interval = QtWidgets.QLabel(self.centralwidget)
        interval.setGeometry(QtCore.QRect(417, 482, 144, 17))
        interval.setStyleSheet("Color: white; background-color: #092c4c; font: 75 13pt \"URW Gothic L\";")
        interval.setAlignment(QtCore.Qt.AlignCenter)
        interval.setObjectName("interval")
        interval.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "interval"))
        self.intervalInput = QtWidgets.QLineEdit(self.centralwidget)
        self.intervalInput.setGeometry(QtCore.QRect(416, 506, 147, 25))
        self.intervalInput.setValidator(QtGui.QIntValidator(0,999999999))
        self.intervalInput.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")
        self.intervalInput.setObjectName("intervalInput")
        self.intervalInput.setText("50")

        self.startAndStopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startAndStopBtn.setGeometry(QtCore.QRect(21, 546, 280, 31))
        self.startAndStopBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startAndStopBtn.setStyleSheet("Color: white; background-color: #0F79DB; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
        self.startAndStopBtn.setObjectName("startAndStopBtn")
        self.ms = QtWidgets.QLabel(self.centralwidget)
        self.ms.setGeometry(QtCore.QRect(567, 514, 27, 17))
        self.ms.setStyleSheet("Color: white; background-color: #092c4c; font: 75 11.5pt \"URW Gothic L\";")
        self.ms.setObjectName("ms")
        self.pauseAndResumeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.pauseAndResumeBtn.setGeometry(QtCore.QRect(312, 546, 281, 31))
        self.pauseAndResumeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pauseAndResumeBtn.setStyleSheet("Color: white; background-color: #808080; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
        self.pauseAndResumeBtn.setObjectName("pauseAndResumeBtn")
        self.pauseAndResumeBtn.setEnabled(False)
        start = QtWidgets.QLabel(self.centralwidget)
        start.setGeometry(QtCore.QRect(29, 482, 176, 17))
        start.setStyleSheet("Color: white; background-color: #092c4c; font: 75 13pt \"URW Gothic L\";")
        start.setAlignment(QtCore.Qt.AlignCenter)
        start.setObjectName("start")
        start.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "start index"))
        self.startIndex = QtWidgets.QLineEdit(self.centralwidget)
        self.startIndex.setGeometry(QtCore.QRect(26, 506, 179, 25))
        self.startIndex.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")
        self.startIndex.setObjectName("startIndex")
        self.startIndex.setValidator(QtGui.QIntValidator(0,999999999))
        label = QtWidgets.QLabel(self.centralwidget)
        label.setGeometry(QtCore.QRect(613, 47, 630, 540))
        label.setStyleSheet("background-color: #092c4c; border-radius: 10px;")
        label.setObjectName("label")
        self.consoleLog = QtWidgets.QTextEdit(self.centralwidget)
        self.consoleLog.setGeometry(QtCore.QRect(624, 114, 610, 464))
        self.consoleLog.setStyleSheet("Color: white; background-color: #3a475a; border: 1.5px solid gray; font: 75 10pt \"URW Gothic L\"; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; border-top-style: none;")
        self.consoleLog.setObjectName("consoleLog")
        self.consoleLog.setReadOnly(True)
        self.consolLog_h = QtWidgets.QLineEdit(self.centralwidget)
        self.consolLog_h.setGeometry(QtCore.QRect(624, 83, 610, 31))
        self.consolLog_h.setStyleSheet(" border-top-right-radius: 5px; border-top-left-radius: 5px; Color: white; background-color: #3a475a; border: 1.5px solid gray; font: 75 11.3pt \"URW Gothic L\"; border-bottom-style: none;")
        self.consolLog_h.setObjectName("consolLog_h")
        self.consolLog_h.setReadOnly(True)
        self.consoleLog.document().setMaximumBlockCount(500)
        self.consoleHeader = QtWidgets.QLabel(self.centralwidget)
        self.consoleHeader.setGeometry(QtCore.QRect(614, 51, 621, 25))
        self.consoleHeader.setStyleSheet("Color: white; background-color: #092c4c; font: 75 13pt \"URW Gothic L\" ; font-weight: 500;")
        self.consoleHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.consoleHeader.setObjectName("consoleHeader")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 7, 71, 35))
        self.logo.setStyleSheet("image: url(\'D:/Users/1027a/Downloads/tmp/logo.png\');")
        self.logo.setObjectName("logo")
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(1168, 55, 61, 22))
        self.clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clear.setStyleSheet("Color: white; background-color: #0F79DB; font-size: 9pt; font-weight: 600; border-radius: 5px;")
        self.clear.setObjectName("clear")
        self.module3 = QtWidgets.QLabel(self.centralwidget)
        self.module3.setGeometry(QtCore.QRect(12, 361, 590, 106))
        self.module3.setStyleSheet("background-color: #092c4c; border-radius: 10px;")
        self.module3.setObjectName("module3")
        self.nomalORnot = QtWidgets.QGroupBox(self.centralwidget)
        self.nomalORnot.setGeometry(QtCore.QRect(22, 365, 181, 95))
        self.nomalORnot.setStyleSheet("Color:white; border-radius: 5px; background-color: #3a475a; font: 75 11pt \"URW Gothic L\";")
        self.nomalORnot.setAlignment(QtCore.Qt.AlignCenter)
        self.nomalORnot.setObjectName("nomalORnot")
        self.nomal = QtWidgets.QRadioButton(self.nomalORnot)
        self.nomal.setGeometry(QtCore.QRect(10, 34, 112, 23))
        self.nomal.setStyleSheet("font: 75 10pt \"URW Gothic L\"; Color: white;")
        self.nomal.setObjectName("nomal")
        self.nomal.setChecked(True)
        self.anomaly = QtWidgets.QRadioButton(self.nomalORnot)
        self.anomaly.setGeometry(QtCore.QRect(10, 64, 112, 23))
        self.anomaly.setStyleSheet("font: 75 10pt \"URW Gothic L\"; Color: white;")
        self.anomaly.setObjectName("anomaly")
        self.subMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.subMenu.setGeometry(QtCore.QRect(212, 365, 381, 95))
        self.subMenu.setStyleSheet("Color:white; border-radius: 5px; background-color: #3a475a; font: 75 11pt \"URW Gothic L\";")
        self.subMenu.setAlignment(QtCore.Qt.AlignCenter)
        self.subMenu.setObjectName("subMenu")
        self.kindOfAnomaly = QtWidgets.QComboBox(self.subMenu)
        self.kindOfAnomaly.setGeometry(QtCore.QRect(35, 34, 131, 27))
        self.kindOfAnomaly.setStyleSheet("background-color: #4A515D; Color: white;")
        self.kindOfAnomaly.setObjectName("kindOfAnomaly")
        self.kindOfAnomaly.addItem("Static")
        self.kindOfAnomaly.addItem("Increase")
        self.kindOfAnomaly.addItem("Decrease")
        self.kindOfAnomaly.hide()
        self.kindOfAnomaly.currentIndexChanged.connect(self.ComboChageSet)
        self.unitInput = QtWidgets.QLineEdit(self.subMenu)
        self.unitInput.setGeometry(QtCore.QRect(175, 34, 161, 28))
        self.unitInput.setStyleSheet("background-color: #4A515D; Color: white; border: 1.5px solid gray; border-radius: 5px;")
        self.unitInput.setObjectName("unitInput")
        self.unitInput.setAlignment(QtCore.Qt.AlignRight)
        self.unitInput.hide()
        self.unit = QtWidgets.QLabel(self.subMenu)
        self.unit.setGeometry(QtCore.QRect(341, 41, 20, 17))
        self.unit.setStyleSheet("Color: white; background-color: #3a475a; font: 75 11.5pt \"URW Gothic L\";")
        self.unit.setObjectName("unit")
        self.unit.hide()
        self.apply = QtWidgets.QPushButton(self.subMenu)
        self.apply.setGeometry(QtCore.QRect(3, 67, 375, 25))
        self.apply.setStyleSheet("Color: white; background-color: #0F79DB; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
        self.apply.setObjectName("apply")
        self.apply.hide()
        self.nextStep = QtWidgets.QLabel(self.subMenu)
        self.nextStep.setGeometry(QtCore.QRect(130, 40, 171, 31))
        self.nextStep.setStyleSheet("font: 75 13pt \"URW Gothic L\";")
        self.nextStep.setObjectName("nextStep")
        CNC_Simulator.setCentralWidget(self.centralwidget)

        self.RetranslateUi(CNC_Simulator)
        self.GiveActionToObject()
        QtCore.QMetaObject.connectSlotsByName(CNC_Simulator)

    def RetranslateUi(self, CNC_Simulator):
        _translate = QtCore.QCoreApplication.translate
        CNC_Simulator.setWindowTitle(_translate("CNC_Simulator", "CNC Simulator - HNinc"))
        self.header.setText(_translate("CNC_Simulator", "CNC Simulator"))
        self.filePath.setText(_translate("CNC_Simulator", "Choose File.."))
        self.browsBtn.setText(_translate("CNC_Simulator", "Open"))
        self.fileInfo.setText(_translate("CNC_Simulator", "File info"))
        self.tilde.setText(_translate("CNC_Simulator", "~"))
        self.startAndStopBtn.setText(_translate("CNC_Simulator", "Start"))
        self.ms.setText(_translate("CNC_Simulator", "ms"))
        self.pauseAndResumeBtn.setText(_translate("CNC_Simulator", "Pause"))
        self.consoleHeader.setText(_translate("CNC_Simulator", "Stream LoadSpindle"))
        self.clear.setText(_translate("CNC_Simulator", "Clear"))
        self.nomalORnot.setTitle(_translate("CNC_Simulator", "choose data type"))
        self.nomal.setText(_translate("CNC_Simulator", "nomal"))
        self.anomaly.setText(_translate("CNC_Simulator", "Anomaly"))
        self.subMenu.setTitle(_translate("CNC_Simulator", "Option"))
        self.nextStep.setText(_translate("CNC_Simulator", "Take the next step"))
        self.consolLog_h.setText(_translate("CNC_Simulator", "  Count,     OpCode,     Time,     LoadSpindle,     Tcode,     TotalCnt,     X,     Y,     Z"))
        self.apply.setText(_translate("CNC_Simulator", "apply"))

    def GiveActionToObject(self):
        self.browsBtn.clicked.connect(self.FileExplorer)
        self.startAndStopBtn.clicked.connect(self.StartAndStopData)
        self.pauseAndResumeBtn.clicked.connect(self.PauseAndResumeData)
        self.clear.clicked.connect(self.ClearConsole)
        self.nomal.clicked.connect(self.AnomalyUiAction)
        self.anomaly.clicked.connect(self.AnomalyUiAction)
        self.apply.clicked.connect(self.ApplyAction)

    def ClearConsole(self):
        self.consoleLog.clear()

    def ComboChageSet(self):
        if self.kindOfAnomaly.currentIndex() == 0:
            self.makeAnomal = False
            self.unit.setText('')
            self.anomalyLog = ''
            self.unitInput.setValidator(QtGui.QIntValidator(0,99999999))
            return
        if self.kindOfAnomaly.currentIndex() > 0:
            self.makeAnomal = False
            self.unit.setText('%')
            self.unitInput.setValidator(QtGui.QIntValidator(0,999))
            return
    
    def AnomalyUiAction(self):
        if self.nomal.isChecked(): 
            self.nextStep.show()
            self.unit.hide()
            self.unitInput.hide()
            self.kindOfAnomaly.hide()
            self.apply.hide()
            self.makeAnomal = False
            self.anomalyLog = ''
        if self.anomaly.isChecked():
            self.nextStep.hide()
            self.unit.show()
            self.unitInput.show()
            self.kindOfAnomaly.show()
            self.apply.show()

    def ApplyAction(self):
        if not self.flag:
            self.error.setText("시뮬레이터가 시작 중인지 확인해주세요.")
            self.error.exec() 
        elif self.unitInput.text() == '':
            self.error.setText("anomaly input을 확인해 주세요.")
            self.error.exec() 
        else:
            self.percent = int(self.unitInput.text())
            if self.kindOfAnomaly.currentIndex() == 2 and self.percent > 100:
                self.error.setText("100%초과하여 데이터를 감소할 수 없습니다.")
                self.error.exec() 
            else:
                self.makeAnomal = True

    def FileExplorer(self):
        FileOpen = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', './', 'csv(*.csv)')
        if FileOpen[0] != '':
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.filePath.setText(FileOpen[0])
            self.ReadData()
            
    def ReadData(self):
        file = open(self.filePath.text(), 'r')
        read = list(csv.reader(file))
        self.data = []
        if len(read[0]) > 13:
            self.data.append(read[0])
            flag = True
            for line in read:
                if flag:
                    flag = False
                else:
                    tmp = line[(len(line)-5):(len(line)-1)]
                    line = line[:(len(line)-5)]
                    flag = True
                    for i in tmp:
                        if flag:
                            flag = False
                        else:
                            if i.find(']') != -1:
                                    i = i.split(']')
                                    i = i[0]
                            line[4] = i
                        self.data.append([i for i in line])
        else:
            self.data = read
        row = (len(self.data))
        column = len(self.data[0])
        self.startIndex.setText('1')
        self.endIndex.setText(str(row))
        info = ' '.join(self.data[0][:11]) + ' .... \n'
        info = info + '  '.join(self.data[1][:11]) + ' .... \n'
        info = info + '  '.join(self.data[2][:11]) + ' .... \n'
        info = info + '  '.join(self.data[3][:11]) + ' .... \n'
        info = info + '  '.join(self.data[4][:11]) + ' .... \n'
        info = info + '  '.join(self.data[5][:11]) + ' .... \n'
        info = info + '  '.join(self.data[6][:11]) + ' .... \n'
        info = info + '  '.join(self.data[7][:11]) + ' .... \n'
        info = info + '  '.join(self.data[8][:11]) + ' .... \n'
        info = info + '  '.join(self.data[9][:11]) + ' .... \n'
        info = info + '  '.join(self.data[10][:11]) + ' .... \n'
        info = info + '  '.join(self.data[11][:11]) + ' .... \n'
        info = info + '  '.join(self.data[12][:11]) + ' .... \n'
        info = info + '  '.join(self.data[13][:11]) + ' .... \n'
        info = info + '...         ...         ...         ...         ...         ...         ...         ...         ...         ...           ... \n'
        info = info + '[ ' + str(row)+' rows X '+ str(column) + ' columns ]'
        self.fileInfo.setText(info)
        QtWidgets.QApplication.restoreOverrideCursor()
        print("Read done")

    def CheckException(self):
        if self.data == None:
            self.error.setText("csv 파일 선택을 먼저 해주세요.")
            self.error.exec()
            return False
        if self.intervalInput.text() == "":
            self.error.setText("interval을 입력해주세요.")
            self.error.exec()
            return False
        if self.startIndex.text() == "":
            self.error.setText("start를 입력해주세요.")
            self.error.exec()
            return False
        if self.endIndex.text() == "":
            self.error.setText("end를 입력해주세요.")
            self.error.exec()
            return False
        if int(self.startIndex.text()) < 1:
            self.error.setText("start의 최소 값은 1입니다.\nstart index를 확인해주세요.")
            self.error.exec()
            return False
        if int(self.endIndex.text()) < int(self.startIndex.text()):
            self.error.setText("end의 최소 값은" + str(int(self.startIndex.text())+1) + "입니다.\nend index를 확인해주세요.")
            self.error.exec()
            return False
        if int(self.intervalInput.text()) < 10:
            self.error.setText("시뮬레이터 성능을 위하여 interval의 최소 값은 10입니다.\ninterval을 확인해주세요.")
            self.error.exec()
            return False
        return True                
    
    def PauseAndResumeData(self):
        check = self.CheckException()
        if check:
            if self.pauseAndResumeBtn.text() == 'Pause':
                self.pauseAndResumeBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Resume"))
                self.flag = False
            else:
                self.pauseAndResumeBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Pause"))
                self.flag = True

    
    def StartAndStopData(self):
        check = self.CheckException()
        if check:
            if self.startAndStopBtn.text() == 'Start':
                self.startAndStopBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Stop"))
                self.startAndStopBtn.setStyleSheet("background-color: #bd253e; Color: white; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
                self.pauseAndResumeBtn.setStyleSheet("background-color: #0F79DB;Color: white; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
                self.pauseAndResumeBtn.setEnabled(True)
                self.start = int(self.startIndex.text())
                self.end = int(self.endIndex.text())
                self.interval = int(self.intervalInput.text())/1000
                self.startIndex.setReadOnly(True)
                self.startIndex.setStyleSheet("background-color: #092c4c; Color: white; border: 1.5px solid gray; border-radius: 5px;")
                self.endIndex.setReadOnly(True)
                self.endIndex.setStyleSheet("background-color: #092c4c; Color: white; border: 1.5px solid gray; border-radius: 5px;")
                self.intervalInput.setReadOnly(True)
                self.intervalInput.setStyleSheet("background-color: #092c4c; Color: white; border: 1.5px solid gray; border-radius: 5px;")
                if self.end <= self.start:
                    self.error.setText("현재 데이터 전송이 시작될 인덱스는 " +str(self.start) + "입니다.\n 시작 인덱스보다 끝 인덱스가 더 작습니다.\n 확인해주세요.")
                    self.error.exec()
                else:
                    self.flag = True
                
            else:       
                self.startAndStopBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Start"))
                self.pauseAndResumeBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Pause"))
                self.startAndStopBtn.setStyleSheet("background-color: #0F79DB; Color: white; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
                self.pauseAndResumeBtn.setEnabled(False)
                self.pauseAndResumeBtn.setStyleSheet("background-color: #808080;Color: white; font: 75 13pt \"URW Gothic L\"; font-weight: 600; border-radius: 7px;")
                self.flag = False
                self.logs = self.logs[:-1]
                self.consoleLog.append(self.logs)
                self.consoleLog.moveCursor(QtGui.QTextCursor.End)
                self.logs = ''
                self.startIndex.setReadOnly(False)
                self.startIndex.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")
                self.endIndex.setReadOnly(False)
                self.endIndex.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")
                self.intervalInput.setReadOnly(False)
                self.intervalInput.setStyleSheet("background-color: #3a475a; Color: white; border: 1.5px solid gray; border-radius: 5px;")

    def SendData(self): 
        sendInterval = 0
        while True:
            if self.flag:
                if self.end >= self.start:
                    timeCurrent = time.time()
                    line = self.data[self.start]
                    if self.makeAnomal:
                        index = self.kindOfAnomaly.currentIndex()
                        if index > 0:
                            if index == 1:
                                trans = int(int(line[4]) * ((self.percent/100)+1))
                                self.anomalyLog = 'Anomaly Mode(Increase):: LoadSpindle Value is changed ' + line[4] + ' ==> ' + str(trans) +'\n'
                            else:
                                trans = int(int(line[4]) * (1-(self.percent/100) ))
                                self.anomalyLog = 'Anomaly Mode(Decrease):: LoadSpindle Value is changed ' + line[4] + ' ==> ' + str(trans) +'\n'
                            line[4] = str(trans)
                        else: 
                            self.anomalyLog = 'Anomaly Mode(Static):: LoadSpindle Value is changed ' + line[4] + ' ==> ' + str(self.percent) +'\n'
                            line[4] = str(self.percent)
                    line[1] = str(timeCurrent * 1000)
                    self.logs = self.logs + str(self.start) + '. ' + line[0] + ', ' + time.strftime('%Y-%m-%d %H:%M:%S.{}'.format(str(timeCurrent).split('.')[1][:3]), time.localtime(timeCurrent)) + ', ' + line[4] + ', ' + line[8] + ', ' + line[-4] + ', ' + line[-3]+ ', ' + line[-2] + ', ' + line[-1] + '\n' + self.anomalyLog
                    send = ','.join(line)
                    sendInterval += self.interval
                    send = send.encode('utf-8')
                    self.producer.send(self.topic,send)
                    self.start += 1
                    if self.end-self.start < 0.999/self.interval or sendInterval > 0.999:
                        if self.logs != '':
                            sendInterval = 0
                            self.logs = self.logs[:-1]
                            self.consoleLog.append(self.logs)
                            self.consoleLog.moveCursor(QtGui.QTextCursor.End)
                            self.logs = ''

                else: # 전송이 완료되었을 때
                    self.consoleLog.append(str(self.end - self.startTmp +1 )+'개의 데이터를 전송을 완료했습니다.')
                    self.start = self.startTmp
                    self.startAndStopBtn.setText(QtCore.QCoreApplication.translate("CNC_Simulator", "Stop"))
                    self.StartAndStopData()
            time.sleep(self.interval)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    CNC_Simulator = QtWidgets.QMainWindow()
    ui = Ui_CNC_Simulator()
    ui.setupUi(CNC_Simulator)
    CNC_Simulator.show()
    os._exit(app.exec_())
