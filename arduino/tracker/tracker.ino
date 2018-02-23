const byte pinEchoL = 7;
const byte pinEchoR = 6;
const byte pinTrig = 5;
int direction = 1;
long diff = 0;
int turnAdjustment = 0;
const String requestSync = "$";
const String ackSync = "&";

void setup() {
 // switch on the radio
 pinMode(8,OUTPUT); 
 digitalWrite(8,HIGH);
 pinMode(4, OUTPUT);
 digitalWrite(4, LOW);
 Serial.begin(115200);
  
  //tracking pins
 pinMode(pinTrig, OUTPUT);
 pinMode(pinEchoL, INPUT);
 pinMode(pinEchoR, INPUT);
}

int getDirection(long diff) {
  if (diff < 0) return -1;
  if (diff > 0) return 1;
  return 0;
}

void loop() {
  /*long newdiff = 0;
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
  diff = newdiff;//*/
  //recordDifference();
  /*if (diff < 0) { Serial.print("L "); Serial.println(turnAdjustment);}
  else if (diff > 0){ Serial.print("R "); Serial.println(turnAdjustment);} 
  else Serial.println("N");//*/
  //delay(1000);
}

void listen() {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
}

long recordDifference() {
  boolean lFire = false;
  boolean rFire = false;
  long lPoint = 0;
  long rPoint=0;
  //Serial.println("Synchronizing....");
  
  //Serial.println("Done!");
  listen();
  while (sync()==-1);
  //wait till echo pin goes up
  //Serial.println("Wait E pin....");
  //while ((digitalRead(pinEchoR) == 0));
  delayMicroseconds(600);
  //Serial.println("E pin up!");
  long startTime = micros();
  //Serial.println("Tracking....");
  while (!rFire){
  //while (!lFire || !rFire){
    //Serial.println(digitalRead(pinEchoR));
    if ((digitalRead(pinEchoR) == LOW) && !rFire){
      Serial.println("RF!");
      rFire = true;
      rPoint = micros() - startTime;
    }
    /*if ((digitalRead(pinEchoL) == LOW) && !lFire){
      //Serial.println("LF!");
      lFire = true;
      lPoint = micros() - startTime;
    }*/
  }
  //Serial.println(rPoint*0.34);
  if (lPoint > 110000 || rPoint > 110000) return 0;
  //Serial.println(lPoint- rPoint);
  return lPoint- rPoint;
}

long sync() {
  long start = micros();
  Serial.print(requestSync);
  Serial.flush();
  if (Serial.find("&")) {
    return micros() - start;
  }
  return -1;
}

