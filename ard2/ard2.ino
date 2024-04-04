#include "Arduino_LED_Matrix.h"

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
ArduinoLEDMatrix matrix;

// Serial and pin setup
void setup() {
  analog_out_val = 2000; // mV
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

  matrix.begin();
}

void loop() {
  det = digitalRead(PinIn); // 0 se superar threshold, 1 caso contrario
  //Serial.println(det);

  if (!det){
    
    timestamp = millis();
    Serial.println(timestamp - timestamp_ant); // ignoramos as medicoes realizadas na primeira hora
    timestamp_ant = millis();
    displayAnimation();

    delay(1000);
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

// Declaração das animações
const uint32_t animation1[][3] = {
	{ 
    0x10000000,
    0x0, 
    0x0
	},
	{ 
    0x10008000, 
    0x0, 
    0x0
	},
	{ 
    0x10008004, 
    0x0, 
    0x0
	},
	{
		0x8004,
		0x200000,
		0x0
	},
	{
		0x4,
		0x200100,
		0x0
	},
	{
		0x0,
		0x200100,
		0x8000000
	},
	{
		0x0,
		0x100,
		0x8004000
	},
	{
		0x0,
		0x0,
		0x8004002
	},
	{
		0x0,
		0x0,
		0x4002
	},
	{
		0x0,
		0x0,
		0x2
	},
	{
		0x0,
		0x0,
		0x0
	}
};
const uint32_t animation2[][3] = {
	{
		0x40000000,
		0x0,
		0x0
	},
	{
		0x40020000,
		0x0,
		0x0
	},
	{
		0x40020010,
		0x0,
		0x0
	},
	{
		0x20010,
		0x800000,
		0x0
	},
	{
		0x10,
		0x800400,
		0x0
	},
	{
		0x0,
		0x800400,
		0x20000000
	},
	{
		0x0,
		0x400,
		0x20010000
	},
	{
		0x0,
		0x0,
		0x20010008
	},
	{
		0x0,
		0x0,
		0x10008
	},
	{
		0x0,
		0x0,
		0x8
	},
	{
		0x0,
		0x0,
		0x0
	}
};
const uint32_t animation3[][3] = {
	{
		0x800000,
		0x0,
		0x0
	},
	{
		0x801000,
		0x0,
		0x0
	},
	{
		0x801002,
		0x0,
		0x0
	},
	{
		0x1002,
		0x400000,
		0x0
	},
	{
		0x2,
		0x400800,
		0x0
	},
	{
		0x0,
		0x400801,
		0x0
	},
	{
		0x0,
		0x801,
		0x200000
	},
	{
		0x0,
		0x1,
		0x200400
	},
	{
		0x0,
		0x0,
		0x200400
	},
	{
		0x0,
		0x0,
		0x400
	},
	{
		0x0,
		0x0,
		0x0
	}
};
const uint32_t animation4[][3] = {
	{
		0x4000000,
		0x0,
		0x0
	},
	{
		0x4008000,
		0x0,
		0x0
	},
	{
		0x4008010,
		0x0,
		0x0
	},
	{
		0x8010,
		0x2000000,
		0x0
	},
	{
		0x10,
		0x2004000,
		0x0
	},
	{
		0x0,
		0x2004008,
		0x0
	},
	{
		0x0,
		0x4008,
		0x0
	},
	{
		0x0,
		0x8,
		0x0
	},
	{
		0x0,
		0x0,
		0x0
	},
	{
		0x0,
		0x0,
		0x0
	},
	{
		0x0,
		0x0,
		0x0
	}
};
const uint32_t animation5[][3] = {
	{
		0x4000000,
		0x0,
		0x0
	},
	{
		0x4004000,
		0x0,
		0x0
	},
	{
		0x4004002,
		0x0,
		0x0
	},
	{
		0x4002,
		0x200000,
		0x0

	},
	{
		0x2,
		0x200100,
		0x0

	},
	{
		0x0,
		0x200100,
		0x10000000

	},
	{
		0x0,
		0x100,
		0x10008000

	},
	{
		0x0,
		0x0,
		0x10008008

	},
	{
		0x0,
		0x0,
		0x8008

	},
	{
		0x0,
		0x0,
		0x8

	},
	{
		0x0,
		0x0,
		0x0

	}
};
const uint32_t animation6[][3] = {
	{
		0x20000000,
		0x0,
		0x0

	},
	{
		0x20020000,
		0x0,
		0x0

	},
	{
		0x20020020,
		0x0,
		0x0

	},
	{
		0x20020,
		0x2000000,
		0x0

	},
	{
		0x20,
		0x2001000,
		0x0

	},
	{
		0x0,
		0x2001001,
		0x0

	},
	{
		0x0,
		0x1001,
		0x100000

	},
	{
		0x0,
		0x1,
		0x100100

	},
	{
		0x0,
		0x0,
		0x100100

	},
	{
		0x0,
		0x0,
		0x100

	},
	{
		0x0,
		0x0,
		0x0

	}
};

const uint32_t (*animations[6])[3] = {animation1, animation2, animation3, animation4, animation5, animation6};

void displayAnimation() {
  int random_number = random(0, 6); // Randomly select an animation index
  // Display the selected animation
  for (int i = 0; i < 11; i++) {
    matrix.loadFrame(animations[random_number][i]);
    delay(20); // Delay between frames
  }
}