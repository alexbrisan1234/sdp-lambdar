long pinTimes[] = {0L, 0L, 0L, 0L};
int pinMapping = {0, 1, 2, 3};
int received = 0;

long const kTimeout = 10000;
long const kDelay = 50000;
long listen_start_time = 0;
/*
 * This is a dummy implementation. We should define when we want to listen and when not
 */
int ShouldListen()
{
  return 1;
}

/*
 * This function reads pins until it receives a on on either one of the 4 pins.
 */
void ReadUntilReceived()
{
  for(;;)
  {
    for (int i = 0 ; i < 4 ; ++i)
    {
      if (digitalRead(pinMapping[i]))
      {
	received = 1;
	return;
      }
    }
  }
}

/*
 * This attempts to read the pin 10 times and it stops when it has read one.
 */
int ReadAllPins()
{
  int read_pins = 0;
  for (int i = 0 ; i < 10 ; ++i)
  {
    for (int pin = 0 ; pin < 4 ; ++pin)
    {
      // We don't want to redo pins that have already been read;
      if (!pinTimes[pin] && digitalRead(pinMapping[pin]))
      {
	pinTimes[pin] = micros();
	++read_pins;
      }
    }
  }
  return read_pins;
}

// Should we wait ? I.e. instead of going to the next main loop
int ShouldWait()
{
  return 0;
}

/*
 * This is the main loop
 */

void MainLoop()
{
  // We should listen to a signal from the user
  if (ShouldListen())
  {
    long listening_for = 0;
    long cur_time = 0;
    int read_pins = 0;
    // Use a timeout to make sure we don't run into an infinite loop
    while (listening_for < kTimeout)
    {
      listen_start_time = micros();
      // We want at least three read pins
      if (ReadAllPins() < 3)
      {
	cur_time = micros();
	listening_for += (cur_time - listen_start_time);
	listen_start_time = cur_time;
	// Reset the times as they won't be in sync next time we listen
	for (int i = 0 ; i < 4 ; ++i)
	{
	  pinTimes[i] = 0;
	}
      }
      else
      {
	/* We have enough information, so we can compute the angle of direction */
      }
    }
  }
  else if(!ShouldWait())
  {
    /* This is the do stuff approach */
  }
  else
  {
    delay(kDelay);
  }
}
// Setup 
void setup() 
{
  for(int i = 0 ; i < 4 ; ++i)
  {
    pinMode(i, INPUT);
  }
  
  Serial.begin(9600);
}
// Main loop
void loop() 
{
  if (!received)
  {
    ReadUntilReceived();
  }
  else
  {
    MainLoop();  
  }
}


