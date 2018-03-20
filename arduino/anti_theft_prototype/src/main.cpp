#include <Arduino.h>

constexpr int kPin = 13;
int last_state;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(kPin, INPUT_PULLUP);
    last_state = digitalRead(kPin);
}

void loop() {
    // put your main code here, to run repeatedly:
    int state = digitalRead(kPin);
    if (last_state != state)
        if (state == HIGH)
            Serial.println("Lid opened");
        else
            Serial.println("Lid closed");
    last_state = state;
    delay(10);
}