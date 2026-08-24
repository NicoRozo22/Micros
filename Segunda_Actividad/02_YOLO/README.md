# 02 - YOLO

## Objetivo

Revisar el funcionamiento de YOLO para la detección de objetos mediante una cámara.

## ¿Qué es YOLO?

YOLO (You Only Look Once) es un modelo de visión por computador utilizado para detectar objetos en imágenes y video en tiempo real.

El modelo analiza cada imagen y determina qué objetos están presentes, indicando su ubicación y nivel de confianza.

## Implementación

Se utilizó Python, OpenCV y Ultralytics YOLO para realizar la detección mediante la cámara del computador.

Durante las pruebas se verificó la detección de diferentes objetos, incluyendo:

- Persona
- Carro
- Motocicleta

## Funcionamiento

1. La cámara captura el video.
2. YOLO procesa cada cuadro.
3. El modelo identifica los objetos.
4. Se muestra un cuadro alrededor de cada objeto detectado.
5. Se indica el nombre del objeto y su nivel de confianza.

## Herramientas utilizadas

- Python
- YOLO
- Ultralytics
- OpenCV
- Cámara

## Archivo principal

`prueba_yolo.py`

Este programa permite realizar la detección de objetos utilizando la cámara en tiempo real.
