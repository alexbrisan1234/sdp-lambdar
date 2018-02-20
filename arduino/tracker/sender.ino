const byte pinTrig = 7;

void setup(){
Serial.begin(115200);
pinMode(8,OUTPUT); // switch on the radio
digitalWrite(8,HIGH);
pinMode(4,OUTPUT); // switch on the radio
digitalWrite(4,LOW); // ensure the radio is not sleeping
pinMode(pinTrig, OUTPUT);
}

void listen(){
 digitalWrite(pinTrig, LOW);
 delayMicroseconds(2);
 digitalWrite(pinTrig, HIGH);
 delayMicroseconds(10);
 digitalWrite(pinTrig, LOW);
}

void loop(){
 
 while(!Serial.find("$"));
 Serial.println("&");
 Serial.flush();
 delay(23);
 listen();
 
}
