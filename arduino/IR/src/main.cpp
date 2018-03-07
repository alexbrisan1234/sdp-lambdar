#include <Arduino.h>

// IR Settings
const int kNrIRSensors = 3;
const int kIRLowerBound = 5;
const int kIRUpperBound = 75;
int ir_receiver_pins[] = {A0, A1, A2};
uint32_t ir_data[] = {0, 0, 0};

// This ID identifies IR data
const String iID = "I";

// Radio settings
const uint32_t kRadioDelay = 10000;  // Time of radio communication in microseconds
const String kRadioRequestCode = "$$$";

// Comm Settings
// Code for no signal received
const uint32_t kNoSig = 0xFFFFFFFF;
// Code identifies beginning of message
const String kOpenMsg = "<";
// Code identifies end of message
const String kCloseMsg = ">";
const String kLineSep = "|";

/*
 * Converst a voltage to a distance
 */
uint32_t convertVoltageToDistance(int voltage);

/*
 * Listens for IR signal
 */
void listenForIR();

/*
 * Sends IR signal
 */
void sendIRData();

void setup() 
{
  // Radio setup
  pinMode(8,OUTPUT); // switch off the radio
  digitalWrite(8,HIGH);
  pinMode(4,OUTPUT); // switch on the radio
  digitalWrite(4,LOW); // ensure the radio is not sleeping
  Serial.begin(9600);
  sendIRData();
}

void loop() 
{
  // Send data over serial to the ev3 brick
  digitalWrite(8,LOW);
  listenForIR();
  sendIRData();
  delay(1);
  digitalWrite(8,HIGH);
  delay(1000);  // TODO: should probably be removed or reduced
}

/* IR Functions */
uint32_t convertVoltageToDistance(int voltage){
  return (voltage > 20) ? (uint32_t)(4800/(voltage-20)) : kNoSig;
}

void listenForIR(){
  int nr_iterations = 5;
  uint32_t distances[nr_iterations][kNrIRSensors];
  for (int iteration = 0 ; iteration < nr_iterations ; ++iteration)
  {
    for (int sensor = 0 ; sensor < kNrIRSensors ; ++sensor)
    {
      distances[iteration][sensor] = convertVoltageToDistance(analogRead(ir_receiver_pins[sensor]));
    }
  }
  
  double means[] = {0.0, 0.0, 0.0};
  // uint32_t variances[] = {0.0, 0.0, 0.0};


  for (int row = 0 ; row < nr_iterations ; ++row)
  {
    for (int col = 0 ; col < kNrIRSensors ; ++col)
    {
      means[col] += distances[row][col] / nr_iterations;
      // variances[col] += (distances[row][col] - means[col]) *  (distances[row][col] - means[col]) / nr_iterations;
    }
  }

  for(int i = 0; i < kNrIRSensors; i++ ){
    // float epsilon = 1.0;
    // if (variances[i] > epsilon)
    // {
    //   ir_data[i] = kNoSig;
    // }
    // else
    // {
    //   ir_data[i] = (uint32_t) means[i];
    // }
    if (means[i] > kIRUpperBound || means[i] < kIRLowerBound) ir_data[i] = kNoSig;
    else ir_data[i] = (uint32_t) means[i];
  }
}

void sendIRData(){
  Serial.print(kOpenMsg);
  Serial.print(iID);
  for(int i = 0; i < kNrIRSensors - 1; ++i){
    Serial.print(ir_data[i]);
    Serial.print(" ");
  }
  Serial.print(ir_data[kNrIRSensors - 1]);
  Serial.print(kCloseMsg);
  Serial.println(kLineSep);
  Serial.flush();
}
