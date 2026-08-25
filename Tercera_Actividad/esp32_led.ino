// ==========================================
// Tercera Actividad - Chatbot Domótico
// Control de un LED mediante comandos de voz
// ESP32
// ==========================================

const int LED_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200);

  Serial.println("ESP32 listo");
  Serial.println("Esperando comandos...");
}

void loop() {

  if (Serial.available() > 0) {

    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "ENCENDER") {

      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED ENCENDIDO");

    }

    else if (comando == "APAGAR") {

      digitalWrite(LED_PIN, LOW);
      Serial.println("LED APAGADO");

    }
  }
}
