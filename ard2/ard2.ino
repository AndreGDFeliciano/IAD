// Parameters
int threshold1 = 21; // bins
int threshold2 = 21; // bins
int debounceTime = 30; // ms

// Sets up pins
int firstAnalogIn  = 15; // A0
int secondAnalogIn  = 16; // A1
// const int PinPwm = 9; // PWM pin

// Declare variables
int initialTime;
int lastPulse = 0; // Está mal na primeira deteçao!
int timeStart;
volatile int det1;
volatile int det2;


void setup() {
	Serial.begin(9600);
	pinMode(firstAnalogIn, INPUT);
	pinMode(secondAnalogIn, INPUT);

  delay(3000); // Delay to start .py code

  timeStart = millis();

  /* PWM
	pinMode(PinOut, OUTPUT);
	pinMode(PinIn, INPUT);
  pinMode(PinPwm, OUTPUT); // Set the PWM pin as an output
  analogWrite(PinPwm, 1); // Set the PWM duty cycle to approximately 5%
  */
}

void loop() {
  det1 = analogRead(firstAnalogIn);
  det2 = analogRead(secondAnalogIn);

  if (det1 > threshold1 && det2 > threshold2) {
    initialTime = millis();
    if (initialTime - lastPulse > debounceTime) {
      // Print output:
      // Peak Value average (mV); Time Stamp (ms); Time between Muons (ms)
      Serial.print((det1+det2)*5000/2048); // mV
      Serial.print(" ");
      Serial.print(initialTime - timeStart); // ms
      Serial.print(" ");
      Serial.print(initialTime - lastPulse); // ms
      Serial.println();

      lastPulse = initialTime;
    }
  }
  delay(0.1);
}
