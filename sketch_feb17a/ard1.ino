const int AnalogIn = A0;
const int ledPin = 13; // LED pin

int comando;
int variable;

void setup() {
	Serial.begin(9600);
	Serial.setTimeout(.1);
}
void loop() {
  if (comando != "1") {
    handleError();
  }
  variable = analogRead(AnalogIn);
	while (!Serial.available());
	comando = Serial.readString().toInt();
	if (comando == 1)Serial.print(variable*5./1024.);
}

void handleError(str errorMessage) {
  Serial.println(errorMessage);
  while(1) { // Start an infinite loop
    digitalWrite(ledPin, HIGH); // Turn the LED on
    delay(250);                 // Wait for 250 milliseconds
    digitalWrite(ledPin, LOW);  // Turn the LED off
    delay(250);                 // Wait for 250 milliseconds
  }
  // No code here will ever execute because of the while(1) loop.
}
