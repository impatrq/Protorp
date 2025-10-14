const int LED_ROJO = 2;
const int LED_AMARILLO = 16;
const int LED_VERDE = 4;

const int VELOCIDAD_MAX = 30;

int velocidad = 0;

void setup() {
  Serial.begin(9600);

  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);

  velocidad = random(10, 60);

  Serial.print("Velocidad inicial: ");
  Serial.print(velocidad);
  Serial.println(" km/h");

  if (velocidad > VELOCIDAD_MAX) {
    digitalWrite(LED_ROJO, HIGH);
    digitalWrite(LED_VERDE, LOW);
  } else {
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, HIGH);
  }

  digitalWrite(LED_AMARILLO, LOW);
}

void loop() {
}