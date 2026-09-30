# ACTIVIDAD 4 - CONTROL DE ILUMINACIÓN MEDIANTE GESTOS

## Universidad Militar Nueva Granada
### Ingeniería Mecatrónica

---

## 1. Descripción del proyecto

En esta actividad se desarrolló un sistema de control de iluminación basado en el reconocimiento de gestos de la mano.

El sistema utiliza una cámara web para capturar la mano y la librería MediaPipe Gesture Recognizer para identificar diferentes gestos. Python procesa la información obtenida y envía comandos mediante comunicación serial a una ESP32.

La ESP32 recibe los comandos y controla tres LEDs, utilizando diferentes niveles de intensidad y dos secuencias de iluminación.

---

## 2. Objetivo

Desarrollar un sistema de control de iluminación mediante gestos de la mano utilizando:

- ESP32
- MediaPipe
- Python
- Cámara web
- Comunicación serial
- Tres LEDs

El sistema permite controlar tres niveles de iluminación y activar dos secuencias diferentes mediante gestos de la mano.

---

## 3. Materiales utilizados

- 1 ESP32
- 1 cámara web
- 2 LEDs verdes
- 1 LED rojo
- 3 resistencias de 220 Ω
- Protoboard
- Cables jumper
- Cable USB
- Computador

---

## 4. Conexiones

Los LEDs fueron conectados a los siguientes pines de la ESP32:

| LED | Color | GPIO | Función |
|---|---|---:|---|
| LED 1 | Verde | GPIO 25 | 30 % |
| LED 2 | Verde | GPIO 26 | 70 % |
| LED 3 | Rojo | GPIO 27 | 100 % |

Cada LED utiliza una resistencia de 220 Ω conectada en serie para limitar la corriente.

Conexiones:

ESP32 GPIO 25 → Resistencia 220 Ω → LED Verde 1 → GND

ESP32 GPIO 26 → Resistencia 220 Ω → LED Verde 2 → GND

ESP32 GPIO 27 → Resistencia 220 Ω → LED Rojo → GND

---

## 5. Gestos utilizados

Los gestos implementados corresponden a los requeridos en la actividad:

| Gesto | MediaPipe | Acción |
|---|---|---|
| Puño cerrado | Closed_Fist | Verde 1 al 30 % |
| Dos dedos en V | Victory | Verde 2 al 70 % |
| Mano abierta | Open_Palm | Rojo al 100 % |
| Pulgar abajo | Thumb_Down | Modo 1 |
| Pulgar arriba | Thumb_Up | Modo 2 |

---

## 6. Control de iluminación

### Puño cerrado - 30 %

Al realizar el gesto de puño cerrado, MediaPipe identifica el gesto Closed_Fist.

Python envía el comando FIST a la ESP32.

La ESP32 enciende el LED verde 1 aproximadamente al 30 % de intensidad.

Gesto: Puño cerrado

Resultado: LED Verde 1 - 30 %

---

### Dos dedos - 70 %

Al realizar el gesto de dos dedos en V, MediaPipe identifica el gesto Victory.

Python envía el comando VICTORY a la ESP32.

La ESP32 enciende el LED verde 2 aproximadamente al 70 % de intensidad.

Gesto: Dos dedos

Resultado: LED Verde 2 - 70 %

---

### Mano abierta - 100 %

Al realizar el gesto de mano abierta, MediaPipe identifica el gesto Open_Palm.

Python envía el comando OPEN a la ESP32.

La ESP32 enciende el LED rojo al 100 % de intensidad.

Gesto: Mano abierta

Resultado: LED Rojo - 100 %

---

## 7. Primera interrupción - Modo 1

El gesto de pulgar abajo, identificado como Thumb_Down, activa el Modo 1.

Python envía el comando MODE1 a la ESP32.

La secuencia implementada es:

LED Verde 1 → LED Rojo → LED Verde 2 → Todos apagados

Esta secuencia permite visualizar el cambio progresivo entre los tres LEDs.

---

## 8. Segunda interrupción - Modo 2

El gesto de pulgar arriba, identificado como Thumb_Up, activa el Modo 2.

Python envía el comando MODE2 a la ESP32.

La secuencia implementada es:

LED Verde 2 → LED Rojo → LED Verde 1 → Todos apagados

El Modo 2 utiliza el orden inverso de los LEDs verdes con respecto al Modo 1.

---

## 9. Funcionamiento general

El funcionamiento del sistema se realiza de la siguiente manera:

1. La cámara web captura la imagen de la mano.
2. MediaPipe analiza la imagen.
3. MediaPipe reconoce el gesto realizado.
4. Python obtiene el nombre del gesto.
5. Python convierte el gesto en un comando.
6. El comando se envía mediante comunicación serial.
7. La ESP32 recibe el comando.
8. La ESP32 ejecuta la función correspondiente.
9. Los LEDs cambian de intensidad o realizan la secuencia indicada.

Flujo general:

Cámara web → MediaPipe → Python → Comunicación Serial → ESP32 → LEDs

---

## 10. Comunicación serial

La comunicación entre Python y la ESP32 utiliza:

Puerto: COM3

Velocidad: 115200 baudios

Los comandos utilizados son:

| Gesto | Comando |
|---|---|
| Closed_Fist | FIST |
| Victory | VICTORY |
| Open_Palm | OPEN |
| Thumb_Down | MODE1 |
| Thumb_Up | MODE2 |
| Finalizar programa | OFF |

---

## 11. Control de intensidad

Los niveles de intensidad fueron implementados mediante valores PWM:

30 % = 77

70 % = 179

100 % = 255

Estos valores se aplican mediante analogWrite() en las salidas correspondientes de la ESP32.

---

## 12. Software utilizado

### Python

Python se utiliza para:

- Capturar la imagen de la cámara.
- Procesar la imagen.
- Utilizar MediaPipe.
- Reconocer los gestos.
- Enviar comandos a la ESP32.

Librerías utilizadas:

- mediapipe
- opencv-python
- pyserial

### MediaPipe

Se utilizó MediaPipe Gesture Recognizer para identificar las posturas de la mano.

El modelo utilizado es:

gesture_recognizer.task

### Arduino IDE

Arduino IDE se utilizó para programar la ESP32.

La ESP32 recibe los comandos enviados por Python y controla los tres LEDs.

---

## 13. Archivos del proyecto

La carpeta de la actividad contiene:

- actividad 4.ino: programa de control de la ESP32.
- gestos_led.py: programa principal de reconocimiento de gestos y comunicación serial.
- prueba_gestos.py: programa utilizado para realizar pruebas de reconocimiento.
- gesture_recognizer.task: modelo utilizado por MediaPipe.
- README.md: documentación del proyecto.

---

## 14. Ejecución del proyecto

1. Conectar la ESP32 al computador mediante USB.

2. Abrir Arduino IDE.

3. Cargar el archivo actividad 4.ino en la ESP32.

4. Cerrar el Monitor Serial de Arduino IDE.

5. Abrir una terminal en la carpeta ACTIVIDAD 4.

6. Ejecutar el programa de Python con el siguiente comando:

py -3.12 gestos_led.py

7. Esperar a que se abra la cámara.

8. Realizar los gestos frente a la cámara.

---

## 15. Resultados obtenidos

Se logró implementar el reconocimiento de los cinco gestos requeridos:

- Puño cerrado.
- Dos dedos en V.
- Mano abierta.
- Pulgar abajo.
- Pulgar arriba.

Se logró establecer correctamente la comunicación entre Python y la ESP32 mediante el puerto serial.

También se comprobó el funcionamiento de los tres niveles de iluminación:

Puño cerrado → Verde 1 → 30 %

Dos dedos → Verde 2 → 70 %

Mano abierta → Rojo → 100 %

Además, se implementaron dos secuencias de iluminación:

Modo 1 → Verde 1 → Rojo → Verde 2 → OFF

Modo 2 → Verde 2 → Rojo → Verde 1 → OFF

---

## 16. Pruebas realizadas

Durante el desarrollo se realizaron pruebas individuales de cada comando mediante comunicación serial.

Los comandos probados fueron:

FIST

VICTORY

OPEN

MODE1

MODE2

OFF

Se comprobó que los LEDs responden correctamente a los comandos.

También se verificó que Python reconoce los gestos mediante la cámara y envía los comandos correspondientes a la ESP32.

El gesto Victory correspondiente a los dos dedos fue probado y configurado para controlar el LED verde 2.

---

## 17. Evidencias

En esta sección se agregarán las evidencias del desarrollo:

- Fotografía del circuito.
- Captura del gesto de puño cerrado.
- Captura del gesto de dos dedos.
- Captura del gesto de mano abierta.
- Captura del gesto de pulgar abajo.
- Captura del gesto de pulgar arriba.
- Video de demostración del funcionamiento.

Video de demostración:

Pendiente de agregar el enlace del video.

---

## 18. Conclusiones

Se desarrolló un sistema de control de iluminación mediante reconocimiento de gestos utilizando una cámara web, MediaPipe, Python y una ESP32.

El sistema permite controlar tres niveles de iluminación mediante los gestos de puño cerrado, dos dedos y mano abierta.

También se implementaron dos modos de secuencia mediante los gestos de pulgar abajo y pulgar arriba.

El proyecto permitió integrar reconocimiento de imágenes, procesamiento de gestos, comunicación serial y control de dispositivos electrónicos mediante una ESP32.

Finalmente, se comprobó el funcionamiento individual de los comandos y del sistema completo.