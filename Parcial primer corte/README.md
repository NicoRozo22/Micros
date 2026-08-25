# Parcial 1 — Figura Casa + Árbol con ESP32

## Descripción

Implementación de una figura de una casa acompañada de un árbol utilizando una ESP32 y un osciloscopio configurado en modo XY.

La ESP32 genera las señales correspondientes a los ejes X y Y mediante sus salidas DAC, permitiendo representar gráficamente la figura en el osciloscopio.

## Objetivo

Diseñar e implementar una figura de CASA + ÁRBOL mediante señales X-Y generadas por una ESP32 y visualizarla utilizando un osciloscopio en modo XY.

## Materiales

- ESP32
- Osciloscopio
- Cables de conexión
- Computador
- Arduino IDE

## Funcionamiento

La ESP32 utiliza dos salidas DAC:

- GPIO 25 → eje X
- GPIO 26 → eje Y

Las señales son conectadas al osciloscopio configurado en modo XY.

El programa genera diferentes coordenadas y realiza interpolación entre los puntos para construir las líneas de la casa y el árbol.

## Resultado

Se obtuvo correctamente la representación de una casa acompañada de un árbol en el osciloscopio mediante el modo XY.

## Archivos

- `oscilloscope_simple.ino` → Código utilizado en la ESP32.
- `IMAGEN_OSCILOSCOPIO.jpeg` → Evidencia de la figura obtenida.
- `README.md` → Documentación del parcial.
