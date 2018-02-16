long startTime, endTime;
boolean pinState;
long accumulatedTime = 0;
int loopCounter = 0;
int pins[] = {PIN3, PIN4, PIN5, PIN6};
int pinHits[] = {0, 0, 0, 0};

int GetCurrentPin()
{
  return pins[0];
}

void MoveCurrentPinToBack()
{
  int pin1_cop = pins[0];
  for (int i = 0 ; i < 3 ; ++i)
  {
    pins[i] = pins[i+1];
  }
  pins[3] = pin1_cop;
}

void RecordPinHit(int PIN_NUMBER)
{
  ++pinHits[PIN_NUMBER-3];
}

void PrintPinHits()
{
  for (int i = 0 ; i < 4 ; ++i)
  {
    Serial.print("Pin ");
    Serial.print(i + 3);
    Serial.print(" was hit ");
    Serial.print(pinHits[i]);
    Serial.println(" times");
  }
}

void ResetPinHits()
{
  for (int i = 0 ; i < 4 ; ++i)
  {
    pinHits[i] = 0;
  }
}

void setup() 
{
  
  for(int i = 0 ; i < 4 ; ++i)
  {
    pins[i] = i + 3;
    pinMode(pins[i], INPUT);
  }
  
  Serial.begin(9600);
}

void loop() 
{
  delay(100);
  if (loopCounter < 10)
  {
    startTime = micros();
    int result = measureTime();
    if (result > 0)
    {
      accumulatedTime += (endTime - startTime);
      MoveCurrentPinToBack();
      RecordPinHit(result);
    }
  }
  else
  {
    PrintPinHits();
    Serial.print("The average measuring time was ");
    ResetPinHits();
    Serial.println(accumulatedTime / loopCounter);
    accumulatedTime = 0;
    loopCounter = 0;
  }
  ++loopCounter;
}

int measureTime()
{
  int current_pin = GetCurrentPin();
  int i = 0;
  for(;i<10;)
  {
    if (digitalRead(current_pin))
    {
      endTime = micros();
      return current_pin;
    }
    ++i;
  }
  
  return -1;
}

