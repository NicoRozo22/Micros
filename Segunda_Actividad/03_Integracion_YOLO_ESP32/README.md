# 03 - Integración YOLO + ESP32

## Objetivo

Integrar YOLO con un ESP32 para detectar vehículos mediante una cámara y controlar LEDs dependiendo del objeto identificado.

## Descripción

En esta actividad se integró un sistema de visión artificial basado en YOLO con un ESP32.

La cámara captura imágenes y el modelo YOLO analiza los objetos presentes. Cuando se detecta un vehículo específico, Python envía una orden al ESP32 mediante comunicación serial.

## Funcionamiento

### Carro

Cuando YOLO detecta un carro:

**Carro → LED rojo 🔴**

### Motocicleta

Cuando YOLO detecta una motocicleta:

**Motocicleta → LED verde 🟢**

### Sin detección

Cuando no se detecta ninguno de los objetos establecidos, los LEDs permanecen apagados.

## Diagrama de funcionamiento

Cámara  
↓  
YOLO  
↓  
Python  
↓  
Comunicación serial  
↓  
ESP32  
↓  
LED correspondiente

## Herramientas utilizadas

- ESP32
- Python
- YOLO
- OpenCV
- Arduino IDE
- Cámara
- LEDs
- Resistencias
- Cable USB

## Comunicación

La comunicación entre Python y el ESP32 se realiza mediante comunicación serial a través del cable USB.

## Archivos

- `yolo_carro_moto.py`: programa de Python encargado de la detección mediante YOLO y del envío de las órdenes al ESP32.
- `codigo_ESP32.ino`: programa cargado en el ESP32 para recibir las órdenes y controlar los LEDs.
