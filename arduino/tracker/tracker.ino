const byte pinEchoL = 7;
const byte pinEchoR = 6;
const byte pinTrig = 5;
int direction = 1;
long diff = 0;
int turnAdjustment = 0;

void setup() {
 pinMode(pinTrig, OUTPUT);
 pinMode(pinEchoL, INPUT);
 pinMode(pinEchoR, INPUT);
 Serial.begin(9600);
}

int getDirection(long diff) {
  if (diff < 0) return -1;
  if (diff > 0) return 1;
  return 0;
}

void loop() {
  long newdiff = 0;
  for (int i =0; i< 4; i++){
    newdiff += recordDifference()/4;
  }
  
  int newDirection = getDirection(newdiff);
  if (direction == -newDirection) {
    //changed side
    turnAdjustment = 0;
    direction = newDirection;
  } else {
      //turn faster
      if (newdiff > diff) turnAdjustment ++;
      //turn slower
      else if (newdiff < diff) turnAdjustment--;
  }
  diff = newdiff;

  if (diff < 0) { Serial.print("L "); Serial.println(turnAdjustment);}
  else if (diff > 0){ Serial.print("R "); Serial.println(turnAdjustment);} 
  else Serial.println("N");
  
}

void listen() {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
}

long recordDifference() {
  //long timeout = 0;
  boolean lFire = false;
  boolean rFire = false;
  long lPoint = 0;
  long rPoint=0;
  listen();
  //wait till echo pin goes up
  while ((digitalRead(pinEchoR) == 0));
  long startTime = micros();
  while ((lFire == 0) || (rFire == 0)){
    if ((digitalRead(pinEchoR) == 0) && !rFire){
      rFire = true;
      rPoint = micros() - startTime;
    }
    if ((digitalRead(pinEchoL) == 0) && !lFire){
      lFire = true;
      lPoint = micros() - startTime;
    }
  }
  if (lPoint > 110000 || rPoint > 110000) return 0;
  return lPoint- rPoint;
}

