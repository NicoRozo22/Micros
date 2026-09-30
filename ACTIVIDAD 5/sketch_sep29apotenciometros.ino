#include <Keypad.h>

// ======================================================
// POTENCIÓMETROS
// ======================================================

const int POT1 = 34;
const int POT2 = 35;


// ======================================================
// TECLADO 4x4
// Solo utilizaremos:
// R1 + C1 = tecla 1
// R1 + C2 = tecla 2
// ======================================================

const byte FILAS = 1;
const byte COLUMNAS = 2;

char teclas[FILAS][COLUMNAS] = {
  {'1', '2'}
};

byte pinesFilas[FILAS] = {
  13
};

byte pinesColumnas[COLUMNAS] = {
  27,
  32
};

Keypad teclado = Keypad(
  makeKeymap(teclas),
  pinesFilas,
  pinesColumnas,
  FILAS,
  COLUMNAS
);


// ======================================================
// CONFIGURACIÓN
// ======================================================

void setup() {

  Serial.begin(115200);

  analogReadResolution(12);

  pinMode(POT1, INPUT);
  pinMode(POT2, INPUT);
}


// ======================================================
// PROGRAMA PRINCIPAL
// ======================================================

void loop() {

  // ----------------------------------------------------
  // LEER POTENCIÓMETROS
  // ----------------------------------------------------

  int valor1 = analogRead(POT1);
  int valor2 = analogRead(POT2);


  // ----------------------------------------------------
  // ENVIAR POT1,POT2
  // ----------------------------------------------------

  Serial.print(valor1);
  Serial.print(",");
  Serial.println(valor2);


  // ----------------------------------------------------
  // LEER TECLADO
  // ----------------------------------------------------

  char tecla = teclado.getKey();


  if (tecla) {

    // Tecla 1 = abrir
    if (tecla == '1') {

      Serial.println("OPEN");
    }


    // Tecla 2 = cerrar
    if (tecla == '2') {

      Serial.println("CLOSE");
    }
  }


  delay(20);
}