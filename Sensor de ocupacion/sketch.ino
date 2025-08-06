const int botonPin = 4;
const int ledRojoPin = 15;
void setup() {
  pinMode(botonPin, INPUT_PULLUP);
  pinMode(ledRojoPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  bool ocupado = digitalRead(botonPin) == LOW;

  digitalWrite(ledRojoPin, ocupado ? HIGH : LOW);

  if (ocupado) {
    Serial.println("🚨 Tramo ocupado");
  } else {
    Serial.println("✅ Tramo libre");
  }

  delay(50);
}