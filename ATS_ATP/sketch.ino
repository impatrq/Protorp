#include <ESP32Servo.h>


const int SERVO_PIN = 18;
const int LED_VERDE = 4;
const int LED_AMARILLO = 16;
const int LED_ROJO = 2;
const int BOTON_PIN = 14;


Servo servo;
int señal = 0;


void actualizarSeñal(int señal) {
  switch (señal) {
    case 0:
      digitalWrite(LED_VERDE, HIGH);
      digitalWrite(LED_AMARILLO, LOW);
      digitalWrite(LED_ROJO, LOW);
      servo.write(0);
      break;
    case 1:
      digitalWrite(LED_VERDE, LOW);
      digitalWrite(LED_AMARILLO, HIGH);
      digitalWrite(LED_ROJO, LOW);
      servo.write(90);
    case 2:
      digitalWrite(LED_VERDE, LOW);
      digitalWrite(LED_AMARILLO, LOW);
      digitalWrite(LED_ROJO, HIGH);
      servo.write(180);
      break;
  }
}

void setup() {

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(BOTON_PIN, INPUT_PULLUP);


  servo.attach(SERVO_PIN);


  actualizarSeñal(señal);
}

void loop() {
 
  if (digitalRead(BOTON_PIN) == LOW) {
    señal = (señal + 1) % 3;
    actualizarSeñal(señal);
    delay(500);
  }
}