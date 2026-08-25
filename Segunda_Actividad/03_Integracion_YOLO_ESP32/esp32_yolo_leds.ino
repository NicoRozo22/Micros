// =====================================================
// INTEGRACIÓN YOLO + ESP32
// Detección de carro y motocicleta mediante LEDs
// =====================================================

// Pines de los LEDs
const int LED_ROJO = 25;
const int LED_VERDE = 26;

void setup() {

  // Configurar LEDs como salida
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  // Inicialmente ambos apagados
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_VERDE, LOW);

  // Comunicación serial con Python
  Serial.begin(115200);

  Serial.println("ESP32 listo");
}

void loop() {

  // Revisar si llegó información desde Python/YOLO
  if (Serial.available() > 0) {

    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();

    // -----------------------------
    // CARRO → LED ROJO
    // -----------------------------
    if (mensaje == "CARRO") {

      digitalWrite(LED_ROJO, HIGH);
      digitalWrite(LED_VERDE, LOW);

      Serial.println("CARRO DETECTADO");
    }

    // -----------------------------
    // MOTO → LED VERDE
    // -----------------------------
    else if (mensaje == "MOTO") {

      digitalWrite(LED_ROJO, LOW);
      digitalWrite(LED_VERDE, HIGH);

      Serial.println("MOTO DETECTADA");
    }

    // -----------------------------
    // APAGAR LEDs
    // -----------------------------
    else if (mensaje == "OFF") {

      digitalWrite(LED_ROJO, LOW);
      digitalWrite(LED_VERDE, LOW);

      Serial.println("LEDS APAGADOS");
    }
  }
}