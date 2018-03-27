#include <Arduino.h>

const byte pinTrig = 6;

void activateUltrasonic(int trigPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
}

void setup()
{
  Serial.begin(115200);
  pinMode(8,OUTPUT); // switch on the radio
  digitalWrite(8,HIGH);
  pinMode(4,OUTPUT); // switch on the radio
  digitalWrite(4,LOW); // ensure the radio is not sleeping

  pinMode(pinTrig, OUTPUT);
  digitalWrite(pinTrig, LOW);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}

void loop()
{
  while(!Serial.find("$$$"));
  activateUltrasonic(pinTrig);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(20);
  digitalWrite(LED_BUILTIN, LOW);
}
