#define FASTADC 1

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

int valorMaximo = 1023; // Valor máximo de leitura do ADC
int valorDiscriminacao = (2 * valorMaximo) / 3; // Valor de discriminação para aceitação de sinais

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);

  #if FASTADC
    // Configura o prescaler para 16
    sbi(ADCSRA, ADPS2);
    cbi(ADCSRA, ADPS1);
    cbi(ADCSRA, ADPS0);
  #endif

  Serial.println("Inicializacao completa.");
}

void loop() {
  // Lê os sinais dos detectores
  int leituraA0 = analogRead(A0);
  int leituraA1 = analogRead(A1);

  // Verifica se ambas as leituras excedem o valor de discriminação ao mesmo tempo
  if(leituraA0 > valorDiscriminacao && leituraA1 > valorDiscriminacao) {
    unsigned long timestamp = millis(); // Captura o timestamp do evento

    Serial.println("Evento de muao detectado:");
    Serial.print("Timestamp: ");
    Serial.print(timestamp);
    Serial.print(" ms, A0: ");
    Serial.print(leituraA0);
    Serial.print(", A1: ");
    Serial.println(leituraA1);
  }
}
