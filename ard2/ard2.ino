// Parameters
const int threshold1 = 21; // bins
const int threshold2 = 21; // bins
const int debounceTime = 34; // ms
const int coincidenceWindow = 200; // μs

// Sets up pins
int firstAnalogIn  = 15; // A1
int secondAnalogIn  = 16; // A2

// Declare variables
int lastPulseTime = 0; // Wrong first detection
volatile int det1, det2;
volatile int peak1, peak2;
volatile unsigned long timeDet1 = 0, timeDet2 = 0;
unsigned long timeOffset = 0, lastTime = 0;
unsigned long currentTime = 0, correctedTime = 0;

void setup() {
	Serial.begin(9600);
	pinMode(firstAnalogIn, INPUT);
	pinMode(secondAnalogIn, INPUT);

  delay(3000); // Delay to start .py code
}

void loop() {
  currentTime = micros();

  // Check for micros() overflow
  if (currentTime < lastTime) {
    timeOffset += 4294967295;  // 2^32 - 1
  }

  lastTime = currentTime;
  correctedTime = currentTime + timeOffset;

  det1 = analogRead(firstAnalogIn);
  det2 = analogRead(secondAnalogIn);

  if (det1 > threshold1) {
      timeDet1 = correctedTime;
      peak1 = det1;
  }
  if (det2 > threshold2) {
      timeDet2 = correctedTime;
      peak2 = det2;
  }

  // Check the coincidence window
  if (abs((int)(timeDet1 - timeDet2)) <= coincidenceWindow && timeDet1 && timeDet2) {
    // Check debounce time
    if (correctedTime - lastPulseTime > debounceTime*1000) {
      // Print output:
      // Peak Value 1 (mV); Peak Value 2 (mV); Time Stamp (μs); Time between Muons (μs)
      Serial.print(peak1*5000/1024); // mV
      Serial.print(" ");
      Serial.print(peak2*5000/1024); // mV
      Serial.print(" ");
      Serial.print(correctedTime); // μs
      Serial.print(" ");
      Serial.println(correctedTime - lastPulseTime); // μs

      lastPulseTime = correctedTime;
    }
    timeDet1 = 0;
    timeDet2 = 0;
  }
  delayMicroseconds(1);
}
