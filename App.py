import PySide6.QtCore
import sys
import random
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import cv2 as cv
import time,threading
import serial


from WindowCapture import Window_Capture

chat1_img= cv.imread('chat1.jpg',1)

target=chat1_img                #image we want to find from screenshot


screenshot_interval= 5          #screenshot evey 5 seconds
range_level=0                   #range level of motor vibration
screenshot_count=0              #index to count the screenshot that detected message
range1= 30                      #range 1= 0-30s
range2= 60                      #range 2= 30s-60s
range3= 90                      #range 3= 60s-90s
range4= 120                     #range 4= 90s-120s
threshold= 0.80                 #threshold for detect image

bluetooth=serial.Serial('COM4', 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick

# function and class from Qt
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.buttonStart = QPushButton("Start")
        self.buttonEnd = QPushButton("End")

 

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.buttonStart)
        self.layout.addWidget(self.buttonEnd)


        self.buttonStart.clicked.connect(lambda: self.Detection(True))
        self.buttonEnd.clicked.connect(lambda: self.Detection(False))

        # run in thread
        self.th = Thread(self)




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

    def setState(self,startStop):
        self.startStop = startStop

    def run(self):
        while self.startStop:

            Window= Window_Capture(target,threshold)
            Detect_result= Window.getScreenshot()

            if Detect_result==0:
                screenshot_count=0
                print("nothing")
            else:
                if screenshot_count<(range1/screenshot_interval):
                    range_level=1
                    screenshot_count= screenshot_count+1
                    print(range_level)
                elif screenshot_count>=(range1/screenshot_interval) and screenshot_count<(range2/screenshot_interval):
                    range_level=2
                    screenshot_count= screenshot_count+1
                    print(range_level)
                elif  screenshot_count>=(range2/screenshot_interval) and screenshot_count<(range3/screenshot_interval):
                    range_level=3
                    screenshot_count= screenshot_count+1
                    print(range_level)
                    bluetooth.write(tr.encode(str(3)))
                elif screenshot_count >= (range3 / screenshot_interval) and screenshot_count < (range4 / screenshot_interval):
                    range_level= 4
                    screenshot_count = screenshot_count + 1
                    print(range_level)
                else:
                    range_level= 5
                    screenshot_count= screenshot_count+1
                    print(range_level)
            # send range level to arduino        
            bluetooth.write(range_level)
            time.sleep(screenshot_interval)


if __name__ == "__main__":
    app = QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())



