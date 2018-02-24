void activateUltrasonic(int trigPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
}

void requestSignal() {
  Serial.println(kRadioRequestCode);
  Serial.flush();
}

void measureTimes(uint32_t startTime, uint32_t* timeLeft, uint32_t* timeRight)
{
  uint8_t echo = getEcho(kBoth);
  // Both echo pins should still be high
  if (echo != kBoth) {
    //Serial.print("ERROR: Listening too late");
    *timeLeft = 0;
    *timeRight = 0;
    return;
  }

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
