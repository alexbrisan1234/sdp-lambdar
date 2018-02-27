int ir_receiver_pins[] = {A1, A2, A3, A4, A5};

struct IRData {
    float distances[]; 
}IRData;


// This ID identifies IR data
const unsigned long iID = 0xFFFFFFFB;

// Code identifies beginning of message
const unsigned long openMsg = 0xFFFFFFFE;

// Code identifies end of message
const unsigned long closeMsg = 0xFFFFFFFD;

void setup(){
   Serial.begin(9600);
   sendIRData(IRData);
}

void loop(){
   sendIRData(listenForIR());
  
}

float convertVoltageToDistance(int voltage){
  float distance = 6343.85*pow(voltage, -1.15);
  return distance;
}

struct IRData listenForIR(){
  for(int i=0;i<5;i++){
    IRData.distances[i] = convertVoltageToDistance(analogRead(ir_receiver_pins[i]));
  }
  return IRData;
}

void sendIRData(struct IRData){
  Serial.println(String(openMsg));
  Serial.flush();
  Serial.println(String(iID));
  Serial.flush();
  for(int i=0;i<5;i++){
    Serial.println(IRData.distances[i]);
    Serial.flush();
  }
  Serial.println(String(closeMsg));
  Serial.flush();
}
