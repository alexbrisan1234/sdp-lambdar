// Tracking settings
constexpr int trigAllPin = 5;  // All receivers are connected to this pin
constexpr int kLeftEchoPin = 6;  // needs to be between 2 and 7 (inclusive)
constexpr int kRightEchoPin = 7;  // needs to be between 2 and 7 (inclusive)
constexpr uint32_t kReceiverTimeout = 110000;

// Masks for echo pins
constexpr uint8_t kLeft = (1 << kLeftEchoPin);
constexpr uint8_t kRight = (1 << kRightEchoPin);
constexpr uint8_t kBoth = kLeft | kRight;

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

void setup() 
{
  // Radio setup
  pinMode(8,OUTPUT); // switch off the radio
  digitalWrite(8,HIGH);
  pinMode(4,OUTPUT); // switch on the radio
  digitalWrite(4,LOW); // ensure the radio is not sleeping
  Serial.begin(115200);

  // Tracking pins setup
  pinMode(trigAllPin, OUTPUT);
  digitalWrite(trigAllPin, LOW);
  pinMode(kLeftEchoPin, INPUT);
  pinMode(kRightEchoPin, INPUT);
}

void loop() 
{
  activateUltrasonic(trigAllPin);
  delayMicroseconds(600);
  uint32_t t0 = micros();
  // Both echo pins should be high now
  if (getEcho(kBoth) != kBoth)
    Serial.print("ERROR: Unexpected echo state");
  requestSignal();

  // Now we have about 20 ms to do stuff

  uint32_t timeLeft, timeRight;
  measureTimes(t0, &timeLeft, &timeRight);

  // Now we have timeLeft and timeRight. We can send them to EV3 or store them
  // in global variables and send in the next iteration. We can also do other
  // stuff here.

  // Testing code. Prints distance to each receiver in mm.
  digitalWrite(8,LOW);
  Serial.print(timeLeft*0.34);
  Serial.print("\t");
  Serial.println(timeRight*0.34);
  Serial.print("\t");
  Serial.println(((long)timeLeft - (long)timeRight)*0.34);
  Serial.flush();
  delay(1);
  digitalWrite(8,HIGH);

  delay(1000);  // TODO: should probably be removed or reduced
}

void activateUltrasonic(int trigPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
}

void requestSignal() {
  Serial.print(kRadioRequestCode);
  Serial.flush();
}

void measureTimes(uint32_t startTime, uint32_t* timeLeft, uint32_t* timeRight)
{
  uint8_t echo = getEcho(kBoth);
  // Both echo pins should still be high
  if (echo != kBoth)
    Serial.print("ERROR: Listening too late");

  *timeLeft = 0xFFFFFFFF;   // Max number
  *timeRight = 0xFFFFFFFF;  // Max number
  // Wait for echo pins to go low and note times
  while (echo != 0x00) {
    echo = getEcho(kBoth);
    if ((*timeLeft == 0xFFFFFFFF) && ((echo & kLeft) == 0))
      *timeLeft = micros() - startTime;
    if ((*timeRight == 0xFFFFFFFF) && ((echo & kRight) == 0))
      *timeRight = micros() - startTime;
  }

  // Check for timeouts
  if (*timeLeft > kReceiverTimeout) *timeLeft = 0xFFFFFFFF;
  if (*timeRight > kReceiverTimeout) *timeRight = 0xFFFFFFFF;

  // Check radio delay
  if (*timeLeft < kRadioDelay) {
    Serial.print("ERROR: Radio delay too high. timeLeft=");
    Serial.println(*timeLeft);
    *timeLeft = 0xFFFFFFFF;
  }
  if (*timeRight < kRadioDelay) {
    Serial.print("ERROR: Radio delay too high. timeRight=");
    Serial.println(*timeRight);
    *timeRight = 0xFFFFFFFF;
  }

  // Adjust for radio delay
  if (*timeLeft != 0xFFFFFFFF)
    *timeLeft -= kRadioDelay;
  if (*timeRight!= 0xFFFFFFFF)
    *timeRight -= kRadioDelay;
}
