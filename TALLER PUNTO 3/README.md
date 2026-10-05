# PUNTO 3 - CONTROL DE BAXTER CON ESP32 Y CINEMÁTICA INVERSA

## Descripción

En este punto se implementó el control de un robot Baxter utilizando un ESP32 y dos potenciómetros. Los valores de los potenciómetros son enviados desde el ESP32 hacia Python mediante comunicación serial. Python recibe estos valores y los utiliza para modificar la posición objetivo del efector final del robot Baxter. Para conseguir el movimiento del robot se utiliza la cinemática inversa (Inverse Kinematics, IK) mediante la función calculateInverseKinematics() de PyBullet.

## Objetivo

Controlar el movimiento del efector final del robot Baxter mediante dos potenciómetros conectados al ESP32.

La función de cada potenciómetro es:

- Potenciómetro 1 → movimiento en el eje X.
- Potenciómetro 2 → movimiento en el eje Z.
- El eje Y permanece fijo.

De esta manera, el movimiento de los potenciómetros modifica la posición objetivo del brazo y la cinemática inversa calcula las posiciones necesarias de las articulaciones.

## Hardware utilizado

- ESP32 Dev Module
- 2 potenciómetros
- Computador
- Cable USB
- Robot Baxter simulado

## Conexiones

Potenciómetro 1:
VCC → 3.3 V
GND → GND
Señal → GPIO 34

Potenciómetro 2:
VCC → 3.3 V
GND → GND
Señal → GPIO 35

## Funcionamiento

El ESP32 realiza la lectura de los dos potenciómetros mediante el ADC.

El ADC del ESP32 trabaja con una resolución de 12 bits, por lo que los valores obtenidos están aproximadamente entre 0 y 4095.

Estos valores son enviados por el puerto serial utilizando el siguiente formato:

POT,valor1,valor2

Por ejemplo:

POT,1911,2544

Python recibe estos datos y convierte los valores de los potenciómetros en porcentajes.

Posteriormente:

- El Potenciómetro 1 modifica la coordenada X.
- El Potenciómetro 2 modifica la coordenada Z.
- La coordenada Y se mantiene constante.

## Cinemática inversa

La cinemática inversa permite determinar los valores de las articulaciones del robot necesarios para alcanzar una posición determinada del efector final.

En PyBullet se utiliza la función:

p.calculateInverseKinematics()

La posición objetivo se obtiene a partir de los valores enviados por el ESP32.

El programa calcula las posiciones articulares y las aplica al robot mediante control de posición.

## Comunicación

La comunicación entre el ESP32 y Python se realiza mediante comunicación serial.

Configuración utilizada:

Puerto: COM3
Baudrate: 115200

El ESP32 envía continuamente los valores de los potenciómetros y Python los recibe para actualizar la posición del Baxter.

## Archivos

El punto está compuesto por los siguientes archivos:

punto 3 taller
├── README.md
├── baxter_esp32.ino
└── baxter_ik_esp32.py

### baxter_esp32.ino

Programa encargado de:

- Leer los dos potenciómetros.
- Configurar el ADC del ESP32.
- Enviar los valores mediante comunicación serial.

### baxter_ik_esp32.py

Programa encargado de:

- Conectarse al ESP32.
- Recibir los valores de los potenciómetros.
- Cargar el robot Baxter en PyBullet.
- Calcular la cinemática inversa.
- Controlar el movimiento del efector final.
- Actualizar la posición del robot en tiempo real.

## Resultado

Se logró controlar el movimiento del efector final del robot Baxter mediante los dos potenciómetros conectados al ESP32.

El primer potenciómetro permite desplazar el efector final en el eje X y el segundo permite desplazarlo en el eje Z, utilizando cinemática inversa para calcular el movimiento de las articulaciones.