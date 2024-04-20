// Parameters
int threshold1 = 21; // bins
int threshold2 = 21; // bins
int debounceTime = 30; // ms
const int coincidenceWindow = 200; // μs

// Sets up pins
int firstAnalogIn  = 15; // A1
int secondAnalogIn  = 16; // A2

// Declare variables
int initialTime;
int timeStart;
int lastPulse = 0; // Wrong first detection
volatile int det1, det2;
volatile unsigned long timeDet1 = 0, timeDet2 = 0;

void setup() {
	Serial.begin(9600);
	pinMode(firstAnalogIn, INPUT);
	pinMode(secondAnalogIn, INPUT);

  delay(3000); // Delay to start .py code

  timeStart = micros();
  lastPulse = timeStart;
}

void loop() {
  int Time1 = micros();
  det1 = analogRead(firstAnalogIn);
  det2 = analogRead(secondAnalogIn);

  if (det1 > threshold1) {
      timeDet1 = micros();
  }
  if (det2 > threshold2) {
      timeDet2 = micros();
  }

  // Check the coincidence window
  if (abs((int)(timeDet1 - timeDet2)) <= coincidenceWindow && timeDet1 && timeDet2) {
    initialTime = micros();

    // Check debounce time
    if (initialTime - lastPulse > debounceTime*1000) {
      // Print output:
      // Peak Value average (mV); Time Stamp (μs); Time between Muons (μs)
      Serial.print((det1+det2)*5000/2048); // mV
      Serial.print(" ");
      Serial.print(initialTime - timeStart); // μs
      Serial.print(" ");
      Serial.println(initialTime - lastPulse); // μs

      lastPulse = initialTime;
    }
    timeDet1 = 0;
    timeDet2 = 0;
  }
  delay(0.001);
}
