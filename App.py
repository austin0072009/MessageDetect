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
import time

print("Start")
port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick
for i in range(5): #send 5 groups of data to the bluetooth
	print("Ping")

    #What do we want to send to bluetooth?
	bluetooth.write(b"BOOP "+str.encode(str(i)))#These need to be bytes not unicode, plus a number
	input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
	print(input_data.decode())#These are bytes coming in so a decode is needed
	time.sleep(0.1) #A pause between bursts
bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")

#################################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())



