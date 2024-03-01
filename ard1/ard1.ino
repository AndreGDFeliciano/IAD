const int AnalogIn = A0;
const int ledPin = 13;

int comando;
int variable;

void setup() {
	Serial.begin(9600);
	Serial.setTimeout(.1);
	pinMode(ledPin, OUTPUT);
	pinMode(AnalogIn, INPUT);
}
void loop() {
  while (!Serial.available());
	comando = Serial.readString().toInt();
	if (comando == 1) {
    variable = analogRead(AnalogIn);
		Serial.println(variable*5./1024.);
    digitalWrite(ledPin,LOW);
	} else {
    Serial.println("Error: Invalid Command"); // Envia mensagem de erro
    digitalWrite(ledPin,HIGH);
  }
}
