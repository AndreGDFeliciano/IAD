// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

unsigned int StartTime;
unsigned int CurrentTime;

void setup() {
  int start ;
  int i ;
#if FASTADC
// set prescale to 16
  sbi(ADCSRA,ADPS2) ;
  cbi(ADCSRA,ADPS1) ;
  cbi(ADCSRA,ADPS0) ;
#endif
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
// test
  Serial.print("ADCTEST: ") ;
  StartTime = micros() ;
  for (i = 0 ; i < 17000 ; i++) 
    analogRead(A1);
  Serial.print(micros() - StartTime) ;
  Serial.println(" microsec (1700 calls)") ;
}

void loop() {
}