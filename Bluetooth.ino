#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10, 11);//Create a serial connection with TX and RX on these pins
//#define BUFFER_SIZE 64//This will prevent buffer overruns.
//char inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
//int count=0;//This is the number of lines sent in from the python script
//int i=0;
int j=0;
char inChar=-1;
const int motorPin = 3;      //motor transistor is connected to pin 3
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
int buttonState = 0;         // variable for reading the pushbutton status
int holdstop = 0;
int prev=0;

void setup()
{
  Serial.begin(9600);
  serial_connection.begin(9600);
  pinMode(ledPin, OUTPUT); // initialize the LED pin as an output;
  pinMode(motorPin, OUTPUT);// initialize the motor as an output;
  pinMode(buttonPin, INPUT_PULLUP);// initialize the pushbutton pin as an input:  
}

void loop()
{
  
  buttonState=digitalRead(buttonPin); 
  if(serial_connection.available()>0 && buttonState==HIGH)//If there are any bytes then deal with them
  {
    char receive = serial_connection.read(); //Read from Serial Communication
    if(receive == '1') //If received data is 1, turn on the LED and send back the sensor data
    {
      prev=1;
    }
    if(receive == '2') //If received data is 1, turn on the LED and send back the sensor data
    {
      prev=2;
    }
    if(receive == '3') //If received data is 1, turn on the LED and send back the sensor data
    {
      prev=3;
    }
    if(receive == '4') //If received data is 1, turn on the LED and send back the sensor data
    {
      prev=4;
    }
    if(receive == '5') //If received data is 1, turn on the LED and send back the sensor data
    {
      prev=5;
    }
    Serial.println("current intensity:"+String(prev));
    serial_connection.println("Let's do this");//Then send an incrmented string back to the python script
    holdstop=0;
    
  }
  if(prev!=0&&holdstop!=1){
    for (j;j<prev;j++){ 
      buttonState = digitalRead(buttonPin);
      if (buttonState==HIGH){
        digitalWrite(motorPin, HIGH); //vibrate
        digitalWrite(ledPin, HIGH);
        delay(100);  // delay one milisecond
        digitalWrite(motorPin, LOW);  //stop vibrating
        digitalWrite(ledPin, LOW);
        delay((1000/prev)-100); //holtfup
      }
      else{
        digitalWrite(motorPin, LOW);
        digitalWrite(ledPin, LOW);
        if(holdstop==0)holdstop=1;
        break;
      }
    }
    j=0;
  }
}
