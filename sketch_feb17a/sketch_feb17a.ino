const int AnalogIn = A0;

int comando;
int variable;

void setup() {
	Serial.begin(9600);
	Serial.setTimeout(.1);
}
void loop() {

  variable = analogRead(AnalogIn);
	while (!Serial.available());
	comando = Serial.readString().toInt();
	if (comando == 1)Serial.print(variable*5./1024.);
}
