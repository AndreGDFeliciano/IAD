// Parameters
int threshold = 30;
int debounceTime = 10;

// Sets up pins
const int AnalogOut = A0;
const int AnalogIn  = A1;
// const int PinPwm = 9; // PWM pin

// Declare variables
int time_dif = 0;
unsigned long timestamp_ant = 0;
int det;
int initialTime;
int finalTime;
int maxVal;
int lastPulse = 0; // Está mal na primeira deteçao! 
int timeStart;


void setup() {
	Serial.begin(9600);
	pinMode(AnalogIn, INPUT);

  delay(3000); // Delay to start .py code
  
  timeStart = millis();
  timestamp_ant = millis();

  /* PWM
	pinMode(PinOut, OUTPUT);
	pinMode(PinIn, INPUT);
  pinMode(PinPwm, OUTPUT); // Set the PWM pin as an output
  analogWrite(PinPwm, 1); // Set the PWM duty cycle to approximately 5%
  */
}

void loop() {
  time_dif = millis() - timestamp_ant;
  det = analogRead(AnalogIn);

//  if (time_dif > 60000){
//    threshold = threshold + 5; // Increase threshold every 60 seconds
//    timestamp_ant = millis();
//  }

  if (det > threshold && threshold < 100) {
    initialTime = millis();
    prints();
    lastPulse = initialTime;
  }
}

void prints() {
  // Print output:
  // Threshold (mV); Peak Value (mV); Time Stamp (ms); Time between Muons (ms)
  Serial.print(threshold*5000/1024); // mV
  Serial.print(" ");
  Serial.print(det*5000/1024); // mV
  Serial.print(" ");
  Serial.print(initialTime - timeStart); // ms
  Serial.print(" ");
  Serial.print(initialTime - lastPulse); // ms
  Serial.println();
}