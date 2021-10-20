import PySide6.QtCore
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

# function and class from Qt
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

# new class & function add below

#########################################################################
#Python to Arduino

import serial

print("Start")
port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick


#include  zoompyauto.py part
import cv2 as cv
import time
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

Start_stop= True                #control from pyQt GUI
while Start_stop:

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
            #send range level to arduino
            bluetooth.write(tr.encode(str(1)))
        elif screenshot_count>=(range1/screenshot_interval) and screenshot_count<(range2/screenshot_interval):
            range_level=2
            screenshot_count= screenshot_count+1
            print(range_level)
            # send range level to arduino
            bluetooth.write(tr.encode(str(2)))
        elif  screenshot_count>=(range2/screenshot_interval) and screenshot_count<(range3/screenshot_interval):
            range_level=3
            screenshot_count= screenshot_count+1
            print(range_level)
            # send range level to arduino
            bluetooth.write(tr.encode(str(3)))
        elif screenshot_count >= (range3 / screenshot_interval) and screenshot_count < (range4 / screenshot_interval):
            range_level= 4
            screenshot_count = screenshot_count + 1
            print(range_level)
            # send range level to arduino
            bluetooth.write(tr.encode(str(4)))
        else:
            range_level= 5
            screenshot_count= screenshot_count+1
            print(range_level)
            # send range level to arduino
            bluetooth.write(tr.encode(str(5)))

    time.sleep(screenshot_interval)


bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")

#################################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())



