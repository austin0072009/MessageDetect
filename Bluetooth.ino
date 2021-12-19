#include "SoftwareSerial.h"
SoftwareSerial serial_connection(11, 11);//Create a serial connection with TX and RX on these pins
#define BUFFER_SIZE 64//This will prevent buffer overruns.
int inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
inr inint=-1;//Initialie the first character as nothing
int count=0;//This is the number of lines sent in from the python script
int j=0;


const int motorPin = 3;      //motor transistor is connected to pin 3
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
int buttonState = 0;         // variable for reading the pushbutton status
int holdstop = 0;
int prev=0;

void setup()
{
  Serial.begin(9600);//Initialize communications to the serial monitor in the Arduino IDE
  serial_connection.begin(9600);//Initialize communications with the bluetooth module
  pinMode(motorPin, OUTPUT);// initialize the motor as an output;
  pinMode(ledPin, OUTPUT); // initialize the LED pin as an output;
  pinMode(buttonPin, INPUT);// initialize the pushbutton pin as an input:
  Serial.printIn("Started");
}

void loop()
{
  byte byte_count=serial_connection.available();//This gets the number of bytes that were sent by the python script
  buttonState = digitalRead(buttonPin);
  if(byte_count && !buttonState)//If there are any bytes then deal with them
  {
    inint=serial_connection.read();//Read one byte
    prev=inint;
    holdstop=0;
    count++;//Increment the line counter
  }
  if(prev!=0){
    for (j;j<prev;j++){
      buttonState = digitalRead(buttonPin);
      if (buttonState==LOW && holdstop==0){
        digitalWrite(motorPin, HIGH); //vibrate
        digitalWrite(ledPin, HIGH);
        delay(100);  // delay one milisecond
        digitalWrite(motorPin, LOW);  //stop vibrating
        digitalWrite(ledPin, LOW)
        delay((1000/prev)-100); //holtfup
      }
      else{
        digitalWrite(motorPin, LOW);
        digitalWrite(ledPin, LOW)
        if(holdstop==0)holdstop=1;
        prev=0;
        break;
      }
    }
    j=0;
  }
}
