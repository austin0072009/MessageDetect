import PySide6.QtCore
import sys
import random
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget,QGridLayout)
import cv2 as cv
import time,threading
import serial


from WindowCapture import Window_Capture

chat1_img= cv.imread('chat1.jpg',1)
chat2_img = cv.imread('tencentchat.jpg',1)


target=chat1_img                #image we want to find from screenshot


screenshot_interval= 5          #screenshot evey 5 seconds
range_level=0                   #range level of motor vibration
screenshot_count=0              #index to count the screenshot that detected message
range1= 30                      #range 1= 0-30s
range2= 60                      #range 2= 30s-60s
range3= 90                      #range 3= 60s-90s
range4= 120                     #range 4= 90s-120s
threshold= 0.80                 #threshold for detect image
toblu=b'0'

# bluetooth=serial.Serial('COM7', 9600)#Start communications with the bluetooth unit
# print("Connected")
# bluetooth.flushInput() #This gives the bluetooth a little kick
# flblu=1
# function and class from Qt
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        State = 2
        
        self.buttonState1 = QPushButton("Tencent")
        self.buttonState2 = QPushButton("Zoom")
        self.buttonStart = QPushButton("Start")
        self.buttonEnd = QPushButton("End")
        self.textBox = QLineEdit(self)
        

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.buttonStart)
        self.layout.addWidget(self.buttonEnd)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.buttonState1)
        self.layout2.addWidget(self.buttonState2)
        self.layout.addWidget(self.textBox)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.layout2)
        self.main_layout.addLayout(self.layout)

        self.setLayout(self.main_layout)


        self.buttonStart.clicked.connect(lambda: self.Detection(True))
        self.buttonEnd.clicked.connect(lambda: self.Detection(False))
        #self.signal_text_set.connect(self.SetText)
        self.buttonState1.clicked.connect(lambda: self.selectState1(1))
        self.buttonState2.clicked.connect(lambda: self.selectState2(2))
        # run in thread
        self.th = Thread(self)
        self.th.signal_text_set.connect(self.SetText)



    @Slot()
    def Detection(self,startStop):
        if(startStop):
            # if ~flblu:
                # bluetooth=serial.Serial('COM7', 9600)#Start communications with the bluetooth unit
                # print("Connected")
                # bluetooth.flushInput() #This gives the bluetooth a little kick

            self.th.setState(startStop)
            self.th.start()
        else:
            self.th.setState(startStop)
            self.th.terminate()
            time.sleep(1)
            print("Stop")
            # bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
            print("Done")
            # flblu=0

    def SetText(self,str):
        self.textBox.setText(str)

    def selectState1(self,state):
        self.th.setMode(state)
        print("State :" ,state)
        self.buttonState1.setEnabled(False)
        self.buttonState2.setEnabled(True)



    def selectState2(self,state):
        self.th.setMode(state)
        print("State :" ,state)

        self.buttonState2.setEnabled(False)
        self.buttonState1.setEnabled(True)



        
# new class & function add below
class Thread(QThread):
    signal_text_set = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.startStop = None
        self.state = 2

    def setState(self,startStop):
        self.startStop = startStop
    def setMode(self,state):
        self.state = state

    def run(self):
        # State = 1 zoom detect
        # State = 2 Tencent detect
        while self.startStop:

            if(self.state == 2):
                target = chat1_img
            else:
                target = chat2_img
            Window= Window_Capture(target,threshold)
            Detect_result= Window.getScreenshot()
            print(target)
            if Detect_result==0:
                screenshot_count=0
                print("nothing")
                self.signal_text_set.emit("nothing")
            else:
                if screenshot_count<(range1/screenshot_interval):
                    range_level=1
                    # toblu=b'1'
                    screenshot_count= screenshot_count+1
                    print(range_level)
                elif screenshot_count>=(range1/screenshot_interval) and screenshot_count<(range2/screenshot_interval):
                    range_level=2
                    # toblu=b'2'
                    screenshot_count= screenshot_count+1
                    print(range_level)
                elif  screenshot_count>=(range2/screenshot_interval) and screenshot_count<(range3/screenshot_interval):
                    range_level=3
                    # toblu=b'3'
                    screenshot_count= screenshot_count+1
                    print(range_level)
                    # bluetooth.write(tr.encode(str(3)))
                elif screenshot_count >= (range3 / screenshot_interval) and screenshot_count < (range4 / screenshot_interval):
                    range_level= 4
                    # toblu=b'4'  
                    screenshot_count = screenshot_count + 1
                    print(range_level)
                else:
                    range_level= 5
                    # toblu=b'5'
                    screenshot_count= screenshot_count+1
                    print(range_level)
                self.signal_text_set.emit(range_level)

            # send range level to arduino        
            # bluetooth.write(range_level)
            # bluetooth.write(toblu)#bluetooth.write(str.encode(str(i)))
            time.sleep(screenshot_interval)


if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(400,300)
    widget.show()
    sys.exit(app.exec())
   

