import PySide6.QtCore
import sys
import random
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import cv2 as cv
import time,threading
import serial


from WindowCapture import Window_Capture





# function and class from Qt
class MyWidget(QWidget):

    def __init__(self):
        super().__init__()


        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.buttonStart = QPushButton("Start")
        self.buttonEnd = QPushButton("End")

        self.textBox = QLineEdit(self)
 

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.buttonStart)
        self.layout.addWidget(self.buttonEnd)
        self.layout.addWidget(self.textBox)


        self.buttonStart.clicked.connect(lambda: self.Detection(True))
        self.buttonEnd.clicked.connect(lambda: self.Detection(False))
        #self.signal_text_set.connect(self.SetText)

        # run in thread
        self.th = Thread(self)
        #self.th.signal_text_set.connect(self.SetText)



    @Slot()
    def Detection(self,startStop):
        if(startStop):
            self.th.setState(startStop)
            self.th.start()
        else:
            self.th.setState(startStop)
            self.th.terminate()
            time.sleep(1)
            print("Stop")

    def SetText(self,str):
        self.textBox.setText(str)
# new class & function add below

#########################################################################
#Python to Arduino

# import serial

# print("Start")
# port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
# bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
# print("Connected")
# bluetooth.flushInput() #This gives the bluetooth a little kick





# bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
# print("Done")

#################################################################################
class Thread(QThread):



    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.startStop = None
        self.signal_text_set = Signal(str)
        self.chat1_img= cv.imread('chat1.jpg',1)
        self.target=self.chat1_img                #image we want to find from screenshot
        self.screenshot_interval= 5          #screenshot evey 5 seconds
        self.range_level=0                   #range level of motor vibration
        self.screenshot_count=0              #index to count the screenshot that detected message
        self.range1= 30                      #range 1= 0-30s
        self.range2= 60                      #range 2= 30s-60s
        self.range3= 90                      #range 3= 60s-90s
        self.range4= 120                     #range 4= 90s-120s
        self.threshold= 0.80                 #threshold for detect image

    def setState(self,startStop):
        self.startStop = startStop

    def run(self):
        bluetooth=serial.Serial('COM4', 9600)#Start communications with the bluetooth unit
        while self.startStop:
            if bluetooth:print("Connected")
            bluetooth.flushInput() #This gives the bluetooth a little kick
            #input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
            #while input_data.decode()!="Hi from bluetooth":
            #    bluetooth.flushInput()
            #    input_data=bluetooth.readline()
            #print(input_data.decode())#These are bytes coming in so a decode is needed
            Window= Window_Capture(self.target,self.threshold)
            Detect_result= Window.getScreenshot()

            if Detect_result==0:
                self.screenshot_count=0
                print("nothing")
                #self.signal_text_set.emit("nothing")
            else:
                if self.screenshot_count<(self.range1/self.screenshot_interval):
                    self.range_level=1
                    self.screenshot_count= self.screenshot_count+1
                    print(self.range_level)
                elif self.screenshot_count>=(self.range1/self.screenshot_interval) and self.screenshot_count<(self.range2/self.screenshot_interval):
                    self.range_level=2
                    self.screenshot_count= self.screenshot_count+1
                    print(self.range_level)
                elif  self.screenshot_count>=(self.range2/self.screenshot_interval) and self.screenshot_count<(self.range3/self.screenshot_interval):
                    self.range_level=3
                    self.screenshot_count= self.screenshot_count+1
                    print(self.range_level)
                    bluetooth.write(tr.encode(str(3)))
                elif self.screenshot_count >= (self.range3 / self.screenshot_interval) and self.screenshot_count < (self.range4 / self.screenshot_interval):
                    self.range_level= 4
                    self.screenshot_count = self.screenshot_count + 1
                    print(self.range_level)
                else:
                    self.range_level= 5
                    self.screenshot_count= self.screenshot_count+1
                    print(self.range_level)
                #self.signal_text_set.emit(self.range_level)

            # send range level to arduino        
            bluetooth.write(self.range_level)
            time.sleep(self.screenshot_interval)


if __name__ == "__main__":
    
    app = QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())



