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

	variable = analogRead(AnalogIn);
	while (!Serial.available());
	comando = Serial.readString().toInt();
	if (comando == 1) {
		Serial.print(variable*5./1024.);
	} else {
    Serial.println("Erro: comando inválido!"); // Envia mensagem de erro
    while (comando != 1) { // Loop infinito até que comando seja 1
      digitalWrite(ledPin, HIGH); // Acende o LED
      delay(500); // Espera meio segundo
      digitalWrite(ledPin, LOW); // Apaga o LED
      delay(500); // Espera meio segundo

      if (Serial.available()) { // Verifica se há um novo comando disponível
        comando = Serial.readString().toInt(); // Lê o novo comando
      }
    }
  }
}
