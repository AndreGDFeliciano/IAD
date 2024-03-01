// Sets up pins
const int AnalogIn = A0;
const int ledPin = 13;

// Declare variables
int comando;
int variable;

// Serial and pin setup
void setup() {
	Serial.begin(9600);
	Serial.setTimeout(.1);
	pinMode(ledPin, OUTPUT);
	pinMode(AnalogIn, INPUT);
}
void loop() {
	while (!Serial.available()); // Waits for a command from the RaspberryPi
	comando = Serial.readString().toInt();
	if (comando == 1) {
    	variable = analogRead(AnalogIn);
		Serial.println(variable*5./1024.); // Sends input value to RaspberryPi
    	digitalWrite(ledPin,LOW);
	} else {
    	Serial.println("Error: Invalid Command"); // Sends error to RaspberryPi
    	digitalWrite(ledPin,HIGH); // Lights up the LED when error is found
  }
}
