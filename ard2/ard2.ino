// Sets up pins
const int AnalogOut = A0;
const int AnalogIn  = A1;
const int PinOut = 3;
const int PinIn = 4;
const int PinPwm = 9; // PWM pin

int valorMaximo = 1023; // Valor máximo de leitura do ADC
int valorDiscriminacao = (valorMaximo * 2 / 3); // Valor de discriminação para aceitação de sinais

// Declare variables
int comando;
int variable;
int analog_out_bit;
int n_muon;
double analog_out_val;
unsigned long timestamp; // Captura o timestamp do evento
unsigned long timestamp_ant;
bool det;

// Serial and pin setup
void setup() {
  analog_out_val = 4000; // mV
  analog_out_bit = (analog_out_val * 4095/ 5000);
	Serial.begin(9600);
	Serial.setTimeout(.1);
	pinMode(PinOut, OUTPUT);
	pinMode(PinIn, INPUT);
	pinMode(AnalogIn, INPUT);
  pinMode(PinPwm, OUTPUT); // Set the PWM pin as an output
  analogWrite(PinPwm, 1); // Set the PWM duty cycle to approximately 5%
  analogWriteResolution(12); // 12 bits
  analogWrite(AnalogOut,analog_out_bit); // Value = (desired value / 5V) * 4095 (2^12-1)
  Serial.println("Inicializacao completa.");
}

void loop() {
  det = digitalRead(PinIn); // 0 se superar threshold, 1 caso contrario
  //Serial.println(det);

  if (!det){
    timestamp = millis();
    Serial.println(timestamp - timestamp_ant); // ignoramos as medicoes realizadas na primeira hora
    timestamp_ant = millis();
    delay(100);
  }


  // Verifica se ambas as leituras excedem o valor de discriminação ao mesmo tempo
  //if(leituraA0 > valorDiscriminacao && leituraA1 > valorDiscriminacao) {
  //  unsigned long timestamp = millis(); // Captura o timestamp do evento
  //  Serial.println("Evento de muao detectado:");
  //  Serial.print("Timestamp: ");
  //  Serial.print(timestamp);
  //  Serial.print(" ms, A0: ");
  //  Serial.print(leituraA0);
  //  Serial.print(", A1: ");
  //  Serial.println(leituraA1);
  //}
}
