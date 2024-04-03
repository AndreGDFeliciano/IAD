// Sets up pins
const int AnalogOut = A0;
const int AnalogIn  = A1;
const int ledPin = 13;
const int PinOut = 3;
const int pwmPin = 9; // PWM pin


// Declare variables
int comando;
int variable;
int analog_out_bit;
double analog_out_val;

// Serial and pin setup
void setup() {
  analog_out_val = 800; // mV
  analog_out_bit = (analog_out_val * 4095/ 5000);
	Serial.begin(9600);
	Serial.setTimeout(.1);
	pinMode(ledPin, OUTPUT);
	pinMode(PinOut, OUTPUT);
	pinMode(AnalogIn, INPUT);
	pinMode(pwmPin, OUTPUT); // Set the PWM pin as an output
  analogWrite(pwmPin, 13); // Set the PWM duty cycle to approximately 5%
  analogWriteResolution(12); // 12 bits
  analogWrite(AnalogOut,analog_out_bit); // Value = (desired value / 5V) * 4095 (2^12-1)
}

void loop() {
	while (!Serial.available()); // Waits for a command from the RaspberryPi
	comando = Serial.readString().toInt();
	if (comando == 1) {
    	variable = analogRead(AnalogIn);
		Serial.println(variable*5./1.024); // Sends input value to RaspberryPi
    	digitalWrite(ledPin,LOW);
	} else {
    	Serial.println("Error: Invalid Command"); // Sends error to RaspberryPi
    	digitalWrite(ledPin,HIGH); // Lights up the LED when error is found
  }
}
