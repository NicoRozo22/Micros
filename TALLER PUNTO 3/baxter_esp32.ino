#include <Arduino.h>

// ============================================================
// CONFIGURACIÓN DE POTENCIÓMETROS
// ============================================================

const int POT_IZQUIERDO = 34;
const int POT_DERECHO = 35;


// ============================================================
// CONFIGURACIÓN INICIAL
// ============================================================

void setup()
{
    Serial.begin(115200);

    // Resolución ADC de 12 bits
    // Rango: 0 - 4095
    analogReadResolution(12);

    pinMode(POT_IZQUIERDO, INPUT);
    pinMode(POT_DERECHO, INPUT);
}


// ============================================================
// BUCLE PRINCIPAL
// ============================================================

void loop()
{
    // --------------------------------------------------------
    // LEER POTENCIÓMETRO 1
    // GPIO 34
    // --------------------------------------------------------

    int potIzquierdo = analogRead(
        POT_IZQUIERDO
    );


    // --------------------------------------------------------
    // LEER POTENCIÓMETRO 2
    // GPIO 35
    // --------------------------------------------------------

    int potDerecho = analogRead(
        POT_DERECHO
    );


    // --------------------------------------------------------
    // ENVIAR DATOS A PYTHON
    //
    // Formato:
    //
    // POT,valor1,valor2
    //
    // Ejemplo:
    //
    // POT,1915,2544
    // --------------------------------------------------------

    Serial.print("POT,");
    Serial.print(potIzquierdo);
    Serial.print(",");
    Serial.println(potDerecho);


    // --------------------------------------------------------
    // PEQUEÑA PAUSA
    // --------------------------------------------------------

    delay(20);
}