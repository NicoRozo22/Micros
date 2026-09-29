# TALLER PUNTO 1 – REAL-TO-SIM CON 3 DRONES

## 1. Descripción

En esta práctica se desarrolla un sistema Real-to-Sim, donde un sistema físico compuesto por un ESP32 y un teclado matricial 4x4 permite controlar tres drones dentro de un entorno de simulación desarrollado en PyBullet.

El objetivo es desplazar los tres drones desde un lugar A hacia un lugar B y posteriormente hacia un lugar C, utilizando comandos enviados desde el ESP32 mediante comunicación serial.

## 2. Objetivo

Desarrollar una aplicación Real-to-Sim que permita controlar tres drones desde un ESP32 y visualizar sus movimientos dentro del entorno de simulación PyBullet.

El sistema permite:

- Controlar tres drones simultáneamente.
- Desplazar los drones entre diferentes puntos.
- Mantener los drones en formación.
- Utilizar un teclado matricial conectado al ESP32.
- Comunicar el ESP32 con Python mediante comunicación serial.
- Visualizar los movimientos en PyBullet.

## 3. Funcionamiento del sistema

El funcionamiento general del sistema es:

TECLADO 4x4
     |
     v
   ESP32
     |
     | Comunicación Serial USB
     v
  PYTHON
real_to_sim.py
     |
     v
  PYBULLET
     |
     v
  3 DRONES

El usuario presiona una tecla en el teclado conectado al ESP32. El ESP32 envía el carácter correspondiente por comunicación serial al computador.

Python recibe la información y selecciona el destino correspondiente para los tres drones.

## 4. Control mediante el teclado

| Tecla | Acción |
|---|---|
| 1 | Mover los drones al lugar A |
| 2 | Mover los drones al lugar B |
| 3 | Mover los drones al lugar C |
| D | Regresar los drones al lugar A |
| X | Finalizar la simulación |

## 5. Lugares de la simulación

Se definieron tres lugares principales dentro del entorno de PyBullet.

### Lugar A

X = 0.0 m  
Y = 0.0 m  
Z = 0.6 m

### Lugar B

X = 1.2 m  
Y = 0.0 m  
Z = 0.6 m

### Lugar C

X = 1.2 m  
Y = 1.2 m  
Z = 0.6 m

La trayectoria principal de los drones es:

A → B → C

## 6. Formación de los drones

Los tres drones se desplazan manteniendo una formación horizontal.

La formación permite mantener una separación entre los drones durante el desplazamiento.

Drone 1        Drone 2        Drone 3
   |              |              |
   v              v              v
  DRON           DRON           DRON

Los tres drones reciben el mismo destino y conservan sus posiciones relativas dentro de la formación.

## 7. Materiales

### Hardware

- ESP32 Dev Module.
- Teclado matricial 4x4.
- Cable USB.
- Computador.

### Software

- Arduino IDE.
- Visual Studio Code.
- Python 3.12.
- PyBullet.
- gym-pybullet-drones.
- PySerial.
- NumPy.
- Gymnasium.

## 8. Conexiones del teclado al ESP32

| Teclado | ESP32 |
|---|---|
| R1 | GPIO 13 |
| R2 | GPIO 14 |
| R3 | GPIO 25 |
| R4 | GPIO 26 |
| C1 | GPIO 27 |
| C2 | GPIO 32 |
| C3 | GPIO 33 |
| C4 | GPIO 16 |

Configuración de comunicación serial:

Puerto: COM3  
Baudrate: 115200

## 9. Comunicación ESP32 - Python

El ESP32 detecta la tecla presionada y envía el carácter correspondiente mediante comunicación serial.

Ejemplo:

Tecla 1 → ESP32 → Python → Lugar A

Tecla 2 → ESP32 → Python → Lugar B

Tecla 3 → ESP32 → Python → Lugar C

Python recibe el carácter enviado por el ESP32 y establece el punto de destino de los tres drones.

## 10. Control de los drones

La simulación utiliza el entorno CtrlAviary y controladores PID de la biblioteca gym-pybullet-drones.

Cada drone posee su propio controlador y recibe una posición objetivo.

Durante la ejecución, el programa calcula continuamente las acciones de control necesarias para que los drones se desplacen hacia la posición seleccionada.

## 11. Archivo principal

La carpeta del proyecto contiene:

TALLER PUNTO 1/
|
|-- README.md
|
`-- real_to_sim.py

### real_to_sim.py

Es el programa principal de la práctica.

Sus funciones principales son:

1. Establecer comunicación con el ESP32.
2. Crear el entorno de simulación.
3. Crear los tres drones.
4. Definir los puntos A, B y C.
5. Leer los comandos enviados desde el ESP32.
6. Seleccionar el destino.
7. Controlar los tres drones.
8. Mantener la formación durante el desplazamiento.

## 12. Ejecución

Antes de ejecutar el programa se debe conectar el ESP32 al computador.

Es importante cerrar el Monitor Serial del Arduino IDE, debido a que Python utiliza el puerto COM3.

El programa de simulación se ejecuta mediante:

py -3.12 real_to_sim.py

Al ejecutar el programa se abre la ventana de PyBullet y aparecen los tres drones.

Posteriormente se pueden utilizar las teclas del teclado físico:

1 → Lugar A  
2 → Lugar B  
3 → Lugar C  
D → Regreso al lugar A  
X → Salir

## 13. Pruebas realizadas

### Prueba 1 - Lugar A

Se presiona la tecla 1.

Los tres drones se desplazan hacia el lugar A.

### Prueba 2 - Lugar B

Se presiona la tecla 2.

Los tres drones se desplazan hacia el lugar B.

### Prueba 3 - Lugar C

Se presiona la tecla 3.

Los tres drones se desplazan hacia el lugar C.

### Prueba 4 - Regreso

Se presiona la tecla D.

Los tres drones regresan al lugar A.

Las pruebas fueron realizadas correctamente y se verificó el desplazamiento de los tres drones dentro de PyBullet.

## 14. Resultado obtenido

El sistema permite controlar correctamente tres drones mediante el teclado conectado al ESP32.

El flujo completo del sistema es:

ESP32
  |
  v
Teclado 4x4
  |
  v
Comunicación Serial
  |
  v
Python
  |
  v
PyBullet
  |
  v
3 Drones
  |
  v
A → B → C

Los tres drones se desplazan simultáneamente y mantienen su formación durante el movimiento.

## 15. Concepto Real-to-Sim

El concepto Real-to-Sim consiste en utilizar comandos provenientes de un sistema físico para controlar un entorno de simulación.

En este proyecto:

- El teclado y el ESP32 representan el sistema físico.
- La comunicación serial transmite las órdenes.
- Python recibe e interpreta las órdenes.
- PyBullet representa el entorno virtual.
- Los tres drones simulados ejecutan las órdenes recibidas.

De esta manera, una acción realizada físicamente sobre el teclado produce una respuesta dentro del entorno simulado.

## 16. Conclusión

Se desarrolló una aplicación Real-to-Sim para controlar tres drones mediante un ESP32 y un teclado matricial.

Los drones pueden desplazarse entre los lugares A, B y C dentro del entorno PyBullet, manteniendo una formación durante el movimiento.

La práctica permitió integrar conocimientos de:

- Microcontroladores.
- ESP32.
- Comunicación serial.
- Programación en Python.
- Control PID.
- Simulación robótica.
- PyBullet.
- Integración entre hardware y software.

Finalmente, se comprobó que las órdenes realizadas mediante el sistema físico son recibidas correctamente por Python y producen el movimiento correspondiente de los tres drones en el entorno virtual.