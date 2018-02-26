#define BAUD 9600

/* // Tracking settings */
const int trigAllPin = 5;  // All receivers are connected to this pin
const int kLeftEchoPin = 6;  // needs to be between 2 and 7 (inclusive)
const int kRightEchoPin = 7;  // needs to be between 2 and 7 (inclusive)
const uint32_t kReceiverTimeout = 110000;

// Masks for echo pins
const uint8_t kLeft = (1 << kLeftEchoPin);
const uint8_t kRight = (1 << kRightEchoPin);
const uint8_t kBoth = kLeft | kRight;

// Radio settings
const uint32_t kRadioDelay = 10000;  // Time of radio communication in microseconds
const String kRadioRequestCode = "$$$";

/*
 * Used to activate the receivers
 */
void activateUltrasonic(int trigPin);
/*
 * Sends radio signal to user's device to cause it to emit an ultrasonic pulse.
 */
void requestSignal();
/*
 * Waits for signal to be received on both receivers and returns the time since
 * `startTime` it took in the `timeLeft` and `timeRight` pointers. If no signal
 * is received, the respective output is set to 0xFFFFFFFF (2^32 - 1).
 */
void measureTimes(uint32_t startTime, uint32_t* timeLeft, uint32_t* timeRight);
/*
 * Uses port manipulation to read all echo pins (specified by the `mask`)
 * extremely fast (~0.1 us).
 * (`PIND` is a byte containing values of pins 0-7.)
 */
uint8_t getEcho(uint8_t mask) {return PIND & mask;}

const byte pinTrig = 7;

// Code for no signal received
const unsigned long noSig = 0xFFFFFFFF;
// Code identifies beginning of message
const unsigned long openMsg = 0xFFFFFFFE;
// Code identifies end of message
const unsigned long closeMsg = 0xFFFFFFFD;

// This ID identifies ultrasonic data
const unsigned long uID = 0xFFFFFFFC;

struct timeData {
    uint32_t leftUD;
    uint32_t rightUD;
};

void setup(){
    Serial.begin(9600);
    pinMode(8,OUTPUT); // switch on the radio
    digitalWrite(8,LOW);
    pinMode(4,OUTPUT); // switch on the radio
    digitalWrite(4,LOW); // ensure the radio is not sleeping
    Serial.begin(115200);

    // Tracking pins setup
    pinMode(trigAllPin, OUTPUT);
    digitalWrite(trigAllPin, LOW);
    pinMode(kLeftEchoPin, INPUT);
    pinMode(kRightEchoPin, INPUT);
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

    activateUltrasonic(trigAllPin);
    delayMicroseconds(600);
    uint32_t t0 = micros();
    // Both echo pins should be high now
    // if (getEcho(kBoth) != kBoth)
        //Serial.println("ERROR: Unexpected echo state");

    requestSignal();

    // Now we have about 20 ms to do stuff

    uint32_t timeLeft, timeRight;
    measureTimes(t0, &td.leftUD, &td.rightUD);

    // Now we have timeLeft and timeRight. We can send them to EV3 or store them
    // in global variables and send in the next iteration. We can also do other
    // stuff here.

    // Testing code. Prints distance to each receiver in mm.

    return td;
}

void sendData(struct timeData td) {
    Serial.println(String(openMsg));
    Serial.flush();
    Serial.println(String(uID));
    Serial.flush();
    Serial.println(String(td.leftUD));
    Serial.flush();
    Serial.println(String(td.rightUD));
    Serial.flush();
    Serial.println(String(closeMsg));
    Serial.flush();
}


void loop(){
    struct timeData td = genData();

    digitalWrite(8,LOW);

    sendData(td);

    delay(20); 
}
