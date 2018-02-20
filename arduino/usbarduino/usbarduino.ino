short incoming = 0;         // a String to hold incoming data
//boolean stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
}

void loop() {
    // Print incoming number on each iteration
    Serial.println(incoming);
}


