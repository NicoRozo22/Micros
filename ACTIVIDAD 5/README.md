 
# ACTIVIDAD 5 - CONTROL DE BRAZO ROBÓTICO CON ESP32

## 1. Descripción

En esta actividad se desarrolla un sistema de control para un brazo robótico utilizando una ESP32 como dispositivo de adquisición de datos.

La ESP32 recibe la información de dos potenciómetros y de dos teclas de un teclado matricial. Los datos son enviados mediante comunicación serial UART hacia un programa desarrollado en Python.

El programa en Python recibe los datos en tiempo real y controla una simulación del brazo robótico utilizando PyBullet y el archivo URDF proporcionado en el repositorio U_Militar.

## 2. Objetivos

- Programar la ESP32 para realizar la lectura de dos potenciómetros.
- Enviar los datos de los sensores mediante comunicación UART.
- Recibir los datos de la ESP32 utilizando Python.
- Controlar las articulaciones del brazo robótico en PyBullet.
- Controlar la apertura y cierre del gripper mediante el teclado.
- Comprobar la comunicación entre la ESP32 y Python en tiempo real.
- Validar el movimiento de las articulaciones del brazo.

## 3. Componentes utilizados

### Hardware

- ESP32 Dev Module
- 2 potenciómetros de 1 kΩ
- Teclado matricial 4x4
- Computador
- Cables de conexión

### Software

- Arduino IDE
- Python 3.12
- PyBullet
- PySerial
- Visual Studio Code
- Archivo URDF del brazo robótico

## 4. Conexiones de los potenciómetros

### Potenciómetro 1

- Pin lateral → GND
- Pin central → GPIO 34
- Pin lateral → 3.3 V

El potenciómetro 1 controla la primera articulación del brazo.

### Potenciómetro 2

- Pin lateral → GND
- Pin central → GPIO 35
- Pin lateral → 3.3 V

El potenciómetro 2 controla la segunda articulación del brazo.

## 5. Conexión del teclado

Para controlar el gripper se utilizan únicamente dos teclas del teclado matricial.

- R1 → GPIO 13
- C1 → GPIO 27
- C2 → GPIO 32

Las teclas utilizadas son:

- Tecla 1 → abrir gripper
- Tecla 2 → cerrar gripper

## 6. Comunicación UART

La ESP32 se comunica con Python mediante el puerto serial COM3.

La velocidad de comunicación utilizada es de 115200 baudios.

Los datos de los potenciómetros se envían con el formato:

POT1,POT2

Ejemplo:

2048,1980

Cuando se presiona la tecla 1, la ESP32 envía:

OPEN

Cuando se presiona la tecla 2, la ESP32 envía:

CLOSE

## 7. Funcionamiento del sistema

La ESP32 realiza la lectura de los dos potenciómetros utilizando sus entradas analógicas.

El potenciómetro conectado al GPIO 34 controla la primera articulación del brazo.

El potenciómetro conectado al GPIO 35 controla la segunda articulación.

Los valores obtenidos tienen un rango de 0 a 4095 y son enviados mediante comunicación UART hacia Python.

Python recibe estos valores, los convierte en posiciones angulares y controla el brazo robótico mediante PyBullet.

El sistema funciona de la siguiente manera:

ESP32 → Comunicación UART → Python → PyBullet → Brazo robótico

## 8. Control de las articulaciones

### Joint 1

El potenciómetro 1 conectado al GPIO 34 controla la articulación:

joint_1

Rango de movimiento:

-2.5 rad a 2.5 rad

### Joint 2

El potenciómetro 2 conectado al GPIO 35 controla la articulación:

joint_2

Rango de movimiento:

-2.0 rad a 2.0 rad

## 9. Control del gripper

El gripper se controla mediante dos teclas del teclado matricial.

Tecla 1:
Abre el gripper.

La ESP32 envía:

OPEN

Python recibe este comando y mueve los dedos del gripper hacia la posición de apertura.

Tecla 2:
Cierra el gripper.

La ESP32 envía:

CLOSE

Python recibe este comando y mueve los dedos del gripper hacia la posición de cierre.

## 10. Articulaciones del brazo

El archivo brazo.urdf contiene las siguientes articulaciones:

- Joint 0 → joint_1 → Revoluta
- Joint 1 → joint_2 → Revoluta
- Joint 2 → joint_gripper → Prismática
- Joint 3 → joint_dedo_izq → Prismática
- Joint 4 → joint_dedo_der → Prismática

Los potenciómetros controlan joint_1 y joint_2.

Para el control del gripper se utilizan joint_dedo_izq y joint_dedo_der.

## 11. Programa de Python

El programa principal utilizado en esta actividad es:

potenciometros_brazo.py

El programa realiza las siguientes funciones:

1. Conecta Python con la ESP32 mediante COM3.
2. Establece una comunicación de 115200 baudios.
3. Inicia la simulación de PyBullet.
4. Carga el archivo brazo.urdf.
5. Lee los datos enviados por los potenciómetros.
6. Convierte los valores de los potenciómetros en ángulos.
7. Controla las articulaciones del brazo.
8. Recibe los comandos OPEN y CLOSE.
9. Controla la apertura y cierre del gripper.
10. Mantiene la comunicación en tiempo real.

## 12. Ejecución

El programa debe ejecutarse desde la carpeta:

C:\Users\rozob\U_Militar\8) Brazo_URDF

Comando:

py -3.12 potenciometros_brazo.py

Antes de ejecutar Python se debe cerrar el Monitor Serial del Arduino IDE para permitir que Python utilice el puerto COM3.

## 13. Archivos

La carpeta de la actividad contiene:

ACTIVIDAD 5/

- potenciometros_brazo.py
- README.md
- brazo.urdf

El archivo brazo.urdf corresponde al modelo del brazo robótico proporcionado en el repositorio U_Militar y se utiliza para realizar la simulación en PyBullet.

## 14. Pruebas de funcionamiento

### Prueba 1 - Potenciómetro 1

Se gira el potenciómetro conectado al GPIO 34.

Resultado esperado:

La primera articulación del brazo cambia de posición de acuerdo con el movimiento del potenciómetro.

### Prueba 2 - Potenciómetro 2

Se gira el potenciómetro conectado al GPIO 35.

Resultado esperado:

La segunda articulación del brazo cambia de posición.

### Prueba 3 - Apertura del gripper

Se presiona la tecla 1.

Resultado esperado:

El gripper se abre.

### Prueba 4 - Cierre del gripper

Se presiona la tecla 2.

Resultado esperado:

El gripper se cierra.

### Prueba 5 - Comunicación en tiempo real

Mientras se mueven los potenciómetros, Python recibe continuamente los valores enviados por la ESP32.

Ejemplo de información mostrada en la consola:

POT1: 2048 | POT2: 1980 | J1: 0.0 | J2: -0.06

Esto permite comprobar la comunicación en tiempo real entre el sistema físico y la simulación.

## 15. Evidencias

En esta sección se deben agregar las evidencias de la práctica:

- Fotografía del montaje de la ESP32.
- Fotografía de los dos potenciómetros.
- Fotografía de las conexiones del teclado.
- Captura de la simulación del brazo en PyBullet.
- Captura de la comunicación serial.
- Video demostrando el movimiento de las articulaciones.
- Video demostrando la apertura y cierre del gripper.

## 16. Resultados

Se implementó la comunicación entre la ESP32 y el programa desarrollado en Python.

Los dos potenciómetros permiten controlar dos articulaciones del brazo robótico y las teclas 1 y 2 permiten controlar la apertura y cierre del gripper.

La comunicación se realiza mediante UART a 115200 baudios, permitiendo enviar los datos de los sensores y los comandos del teclado hacia Python en tiempo real.

## 17. Conclusión

En esta actividad se desarrolló un sistema de control para un brazo robótico utilizando una ESP32, dos potenciómetros y un teclado matricial.

Los valores de los sensores fueron adquiridos mediante las entradas analógicas GPIO 34 y GPIO 35 y enviados mediante comunicación UART hacia Python.

El programa desarrollado en Python procesa los datos y controla el brazo robótico utilizando PyBullet y el modelo URDF proporcionado.

También se implementó el control del gripper mediante dos teclas, permitiendo realizar las acciones de apertura y cierre.

Finalmente, se comprobó la comunicación en tiempo real entre la ESP32 y la simulación del brazo robótico.