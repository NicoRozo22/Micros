// ============================================================
// ACTIVIDAD 4
// CONTROL DE ILUMINACION MEDIANTE GESTOS
// ESP32 + MEDIAPIPE + PYTHON
// ============================================================


// ============================================================
// PINES
// ============================================================

const int LED_VERDE_1 = 25;
const int LED_ROJO    = 27;
const int LED_VERDE_2 = 26;


// ============================================================
// APAGAR TODOS LOS LED
// ============================================================

void apagarTodos() {

  analogWrite(LED_VERDE_1, 0);
  analogWrite(LED_ROJO, 0);
  analogWrite(LED_VERDE_2, 0);
}


// ============================================================
// 30% DE INTENSIDAD
// PUÑO
// VERDE 1
// ============================================================

void nivel30() {

  apagarTodos();

  analogWrite(LED_VERDE_1, 77);
}


// ============================================================
// 70% DE INTENSIDAD
// DOS DEDOS
// VERDE 2
// ============================================================

void nivel70() {

  apagarTodos();

  analogWrite(LED_VERDE_2, 179);
}


// ============================================================
// 100% DE INTENSIDAD
// MANO ABIERTA
// ROJO
// ============================================================

void nivel100() {

  apagarTodos();

  analogWrite(LED_ROJO, 255);
}


// ============================================================
// MODO 1
// PULGAR ABAJO
//
// SECUENCIA:
// VERDE 1 -> ROJO -> VERDE 2
// ============================================================

void modo1() {

  // --------------------------------
  // PASO 1 - VERDE 1
  // --------------------------------

  apagarTodos();

  analogWrite(LED_VERDE_1, 77);

  delay(600);


  // --------------------------------
  // PASO 2 - ROJO
  // --------------------------------

  apagarTodos();

  analogWrite(LED_ROJO, 255);

  delay(600);


  // --------------------------------
  // PASO 3 - VERDE 2
  // --------------------------------

  apagarTodos();

  analogWrite(LED_VERDE_2, 179);

  delay(600);


  // --------------------------------
  // FINAL
  // --------------------------------

  apagarTodos();

  delay(300);
}


// ============================================================
// MODO 2
// PULGAR ARRIBA
//
// SECUENCIA:
// VERDE 2 -> ROJO -> VERDE 1
// ============================================================

void modo2() {

  // --------------------------------
  // PASO 1 - VERDE 2
  // --------------------------------

  apagarTodos();

  analogWrite(LED_VERDE_2, 179);

  delay(600);


  // --------------------------------
  // PASO 2 - ROJO
  // --------------------------------

  apagarTodos();

  analogWrite(LED_ROJO, 255);

  delay(600);


  // --------------------------------
  // PASO 3 - VERDE 1
  // --------------------------------

  apagarTodos();

  analogWrite(LED_VERDE_1, 77);

  delay(600);


  // --------------------------------
  // FINAL
  // --------------------------------

  apagarTodos();

  delay(300);
}


// ============================================================
// CONFIGURACION
// ============================================================

void setup() {

  Serial.begin(115200);

  pinMode(LED_VERDE_1, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_VERDE_2, OUTPUT);

  apagarTodos();
}


// ============================================================
// PROGRAMA PRINCIPAL
// ============================================================

void loop() {

  if (Serial.available() > 0) {

    String comando = Serial.readStringUntil('\n');

    comando.trim();


    // --------------------------------
    // PUÑO
    // 30%
    // --------------------------------

    if (comando == "FIST") {

      nivel30();
    }


    // --------------------------------
    // DOS DEDOS
    // 70%
    // --------------------------------

    else if (comando == "VICTORY") {

      nivel70();
    }


    // --------------------------------
    // MANO ABIERTA
    // 100%
    // --------------------------------

    else if (comando == "OPEN") {

      nivel100();
    }


    // --------------------------------
    // PULGAR ABAJO
    // MODO 1
    // --------------------------------

    else if (comando == "MODE1") {

      modo1();
    }


    // --------------------------------
    // PULGAR ARRIBA
    // MODO 2
    // --------------------------------

    else if (comando == "MODE2") {

      modo2();
    }


    // --------------------------------
    // APAGAR
    // --------------------------------

    else if (comando == "OFF") {

      apagarTodos();
    }
  }
}