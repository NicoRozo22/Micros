#include <Keypad.h>

// ===============================
// POTENCIOMETROS
// ===============================
const int POT_IZQ = 34;
const int POT_DER = 35;

// ===============================
// TECLADO 1x2
// ===============================
const byte FILAS = 1;
const byte COLUMNAS = 2;

char teclas[FILAS][COLUMNAS] = {
  {'1', '2'}
};

byte pinesFilas[FILAS] = {13};
byte pinesColumnas[COLUMNAS] = {27, 32};

Keypad teclado = Keypad(
  makeKeymap(teclas),
  pinesFilas,
  pinesColumnas,
  FILAS,
  COLUMNAS
);

void setup() {

  Serial.begin(115200);

  analogReadResolution(12);

  pinMode(POT_IZQ, INPUT);
  pinMode(POT_DER, INPUT);
}

void loop() {

  // Leer potenciómetros
  int izquierda = analogRead(POT_IZQ);
  int derecha = analogRead(POT_DER);

  // Enviar:
  // POT,izquierda,derecha
  Serial.print("POT,");
  Serial.print(izquierda);
  Serial.print(",");
  Serial.println(derecha);

  // Leer teclado
  char tecla = teclado.getKey();

  if (tecla == '1') {
    Serial.println("OPEN");
  }

  if (tecla == '2') {
    Serial.println("CLOSE");
  }

  delay(20);
}
