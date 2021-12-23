import time
import serial


bluetooth=serial.Serial('COM7', 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput()
# send range level to arduino        
bluetooth.write(b'4')
#bluetooth.write(str.encode(str(5)))#bluetooth.write(str.encode(str(i)))
input_data=bluetooth.readline()#This reads the incoming data.
print(input_data.decode())#These are bytes coming in so a decode is needed
time.sleep(10) #A pause between bursts
bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")

