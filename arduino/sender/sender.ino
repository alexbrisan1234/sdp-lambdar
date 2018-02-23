const byte pinTrig = 7;

// Code for no signal received
const unsigned long noSig = 4294967295;
// Code identifies beginning of message
const unsigned long openMsg = 4294967294;
// Code identifies end of message
const unsigned long closeMsg = 4294967293;


// This ID identifies ultrasonic data
const unsigned long uID = 4294967292;

struct timeData {
    byte lD;
    byte rD;
};

void setup(){
    Serial.begin(115200);
    pinMode(8,OUTPUT); // switch on the radio
    digitalWrite(8,LOW);
    /* pinMode(4,OUTPUT); // switch on the radio */
    /* digitalWrite(4,LOW); // ensure the radio is not sleeping */
    /* pinMode(pinTrig, OUTPUT); */
}

void listen(){
    digitalWrite(pinTrig, LOW);
    delayMicroseconds(2);
    digitalWrite(pinTrig, HIGH);
    delayMicroseconds(10);
    digitalWrite(pinTrig, LOW);
}

struct timeData genData() {
    struct timeData td;
    td.lD = 5;
    td.rD = 6;

    return td;
}

void sendAsBytes(long i) {
    Serial.write(i);
    Serial.write(i >> 8);
    Serial.write(i >> 16);
    Serial.write(i >> 24);
}

void sendData(struct timeData td) {
    Serial.println(String(openMsg));
    Serial.flush();
    Serial.println(String(uID));
    Serial.flush();
    Serial.println(String(td.lD));
    Serial.flush();
    Serial.println(String(td.rD));
    Serial.flush();
    Serial.println(String(closeMsg));
    Serial.flush();
}


void loop(){
    sendData(genData());
    delay(20); 
}
