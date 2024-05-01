// Parameters
const int threshold1 = 21; // Threshold for detector 1 (bins)
const int threshold2 = 21; // Threshold for detector 1 (bins)
const int debounceTime = 34; // Debounce Time (ms)
const int coincidenceWindow = 500; // Coincidence Window (μs)

// Sets up pins
int firstAnalogIn  = 15; // A1
int secondAnalogIn  = 16; // A2

// Variable Declarations
int lastPulseTime = 0; // Time of last detection
volatile int det1 = 0, det2 = 0; // Current detection values
volatile int maxPeak1 = 0, maxPeak2 = 0; // Maximum values observed
volatile unsigned long long timeDet1 = 0, timeDet2 = 0; // Peak timestamps
unsigned long long timeOffset = 0; // For handling micros() overflow
unsigned long long lastTime = 0; // For handling micros() overflow
unsigned long long currentTime = 0, correctedTime = 0; // Current and adjusted times

void setup() {
	Serial.begin(9600);

  // Pin setup
	pinMode(firstAnalogIn, INPUT);
	pinMode(secondAnalogIn, INPUT);

  delay(3000); // Delay to start .py code
}

void loop() {
  currentTime = micros(); // Update the current time

  // Handles micros() overflow
  if (currentTime < lastTime) {
    timeOffset += 4294967295;  // 2^32 - 1
  }

  lastTime = currentTime;
  correctedTime = currentTime + timeOffset; // Adjusted time considering overflow


  // Read sensor values
  det1 = analogRead(firstAnalogIn);
  det2 = analogRead(secondAnalogIn);

  // Detect new peaks and record their time
  if (det1 > threshold1 && det1 > maxPeak1) {
      maxPeak1 = det1;
      timeDet1 = correctedTime;
  }
  if (det2 > threshold2 && det2 > maxPeak2) {
      maxPeak2 = det2;
      timeDet2 = correctedTime;
  }

  // Check if peaks are inside the coincidence window
  if (abs((int)(timeDet1 - timeDet2)) <= coincidenceWindow && timeDet1 && timeDet2) {
    // Check if pulse isn't within the debounce time to avoid double counts
    if (correctedTime - lastPulseTime > debounceTime*1000) {
      // Print output:
      // Peak Value 1 (mV); Peak Value 2 (mV); Time Stamp (μs); Time between Muons (μs)
      Serial.print(maxPeak1*5000/1024); // mV
      Serial.print(" ");
      Serial.print(maxPeak2*5000/1024); // mV
      Serial.print(" ");
      Serial.print(correctedTime); // μs
      Serial.print(" ");
      Serial.println(correctedTime - lastPulseTime); // μs

      lastPulseTime = correctedTime; // Update time of last event
    }
    // Reset peak values
    maxPeak1 = 0;
    maxPeak2 = 0;
    timeDet1 = 0;
    timeDet2 = 0;
  } else {
    // Reset peaks if outside the coincidence window
    if (timeDet1 && (correctedTime - timeDet1 > coincidenceWindow)) {
      timeDet1 = 0;
      maxPeak1 = 0;
      timeDet2 = 0;
      maxPeak2 = 0;
    }
    else if (timeDet2 && (correctedTime - timeDet2 > coincidenceWindow)) {
      timeDet1 = 0;
      maxPeak1 = 0;
      timeDet2 = 0;
      maxPeak2 = 0;
    }
  }
  delayMicroseconds(1); // Small delay because of CPU
}
