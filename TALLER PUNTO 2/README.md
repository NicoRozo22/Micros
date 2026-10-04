# TALLER PUNTO 2 - CONTROL DE ROBOT BAXTER CON ESP32

## Descripción

En este proyecto se desarrolla una consola de mandos utilizando un ESP32 para controlar un robot Baxter mediante una simulación realizada en PyBullet.

El sistema permite controlar los movimientos de los brazos del robot mediante dos potenciómetros y controlar la apertura y cierre de las pinzas mediante un teclado.

Además, se implementa la interacción con un objeto dentro de la simulación, permitiendo que el robot Baxter pueda agarrarlo y desplazarlo mediante el movimiento de su brazo.

El proyecto busca cumplir con el objetivo de desarrollar una interfaz de control física que permita una movilidad continua del robot y la manipulación de objetos.

---

## Objetivos

- Desarrollar una consola de mandos utilizando un ESP32.
- Controlar el movimiento de los brazos del robot Baxter.
- Utilizar dos potenciómetros para generar movimientos continuos.
- Controlar la apertura y cierre de las pinzas.
- Implementar comunicación serial entre el ESP32 y Python.
- Utilizar PyBullet para realizar la simulación del robot.
- Permitir que el robot Baxter agarre y mueva un objeto.
- Integrar hardware y simulación en un sistema de control.

---

## Hardware utilizado

- ESP32 Dev Module
- 2 potenciómetros de 1 kΩ
- Teclado matricial de 1 fila y 2 columnas
- Cable USB
- Computador

---

## Conexiones del ESP32

### Potenciómetro 1 - Brazo izquierdo

| Terminal del potenciómetro | ESP32 |
|---|---|
| Terminal exterior | GND |
| Terminal central | GPIO 34 |
| Terminal exterior | 3.3 V |

### Potenciómetro 2 - Brazo derecho

| Terminal del potenciómetro | ESP32 |
|---|---|
| Terminal exterior | GND |
| Terminal central | GPIO 35 |
| Terminal exterior | 3.3 V |

Los dos potenciómetros utilizan la alimentación de 3.3 V del ESP32 y comparten GND.

### Teclado

| Terminal del teclado | ESP32 |
|---|---|
| R1 | GPIO 13 |
| C1 | GPIO 27 |
| C2 | GPIO 32 |

### Funciones del teclado

| Tecla | Función |
|---|---|
| 1 | Abrir las pinzas |
| 2 | Cerrar las pinzas y agarrar el objeto |

---

## Funcionamiento general

El ESP32 realiza la lectura de los dos potenciómetros mediante sus entradas ADC.

El ESP32 utiliza una resolución de 12 bits, por lo que los valores obtenidos se encuentran aproximadamente entre:

    0 - 4095

Los valores son enviados mediante comunicación serial al computador utilizando una velocidad de:

    115200 baudios

El formato utilizado para transmitir los valores de los potenciómetros es:

    POT,valor1,valor2

Por ejemplo:

    POT,2048,3000

El programa desarrollado en Python recibe estos datos, interpreta los valores de los potenciómetros y los transforma en posiciones para las articulaciones del robot Baxter dentro de PyBullet.

---

## Control de los brazos

El sistema utiliza dos potenciómetros para controlar los brazos del robot.

### GPIO 34

El potenciómetro conectado al GPIO 34 controla el brazo izquierdo de Baxter.

### GPIO 35

El potenciómetro conectado al GPIO 35 controla el brazo derecho de Baxter.

Los dos potenciómetros trabajan de forma continua, permitiendo modificar la posición de los brazos mientras el usuario gira los controles.

El valor del ADC se transforma a un rango aproximado de:

    -1.5 rad a +1.5 rad

Esto permite realizar el movimiento de los brazos de manera progresiva.

---

## Control de las pinzas

El teclado permite controlar las pinzas del robot mediante dos comandos.

### Tecla 1 - OPEN

Al presionar la tecla 1, el ESP32 envía el comando:

    OPEN

Python recibe este comando y ordena al robot abrir las pinzas.

### Tecla 2 - CLOSE

Al presionar la tecla 2, el ESP32 envía:

    CLOSE

Python recibe el comando, cierra las pinzas y activa el mecanismo de agarre del objeto dentro de la simulación.

---

## Manipulación del objeto

Dentro de la simulación se crea un objeto representado por un cubo.

El objetivo es que Baxter pueda interactuar con este objeto mediante sus pinzas.

Cuando se utiliza el comando de cierre, el programa establece una relación entre el objeto y la mano del robot, permitiendo que el objeto sea desplazado junto con el brazo.

De esta manera se demuestra la capacidad del sistema para:

1. Controlar el brazo.
2. Posicionar la mano.
3. Cerrar la pinza.
4. Agarrar el objeto.
5. Mover el objeto mediante el brazo.

---

## Comunicación entre los sistemas

El funcionamiento completo puede representarse de la siguiente manera:

    ┌───────────────────────┐
    │         ESP32         │
    │                       │
    │  GPIO34 ─ Potenciómetro 1
    │  GPIO35 ─ Potenciómetro 2
    │                       │
    │  GPIO13 ─ Teclado     │
    │  GPIO27 ─ Teclado     │
    │  GPIO32 ─ Teclado     │
    └───────────┬───────────┘
                │
                │ USB / Serial
                │ 115200 baudios
                ▼
    ┌───────────────────────┐
    │         Python        │
    │                       │
    │  Lectura de datos     │
    │  Control de Baxter    │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │       PyBullet        │
    │                       │
    │        BAXTER         │
    │                       │
    │  Brazo izquierdo      │
    │  Brazo derecho        │
    │  Pinzas               │
    │  Objeto               │
    └───────────────────────┘

---

## Software utilizado

- Arduino IDE
- Python 3.12
- PyBullet
- PySerial
- Visual Studio Code

---

## Librerías de Python

El proyecto utiliza principalmente:

    pybullet

para realizar la simulación del robot y:

    pyserial

para establecer la comunicación entre Python y el ESP32.

La instalación puede realizarse mediante:

    py -3.12 -m pip install pybullet-arm64 pyserial

---

## Ejecución del proyecto

### 1. Conectar el ESP32

Conectar el ESP32 al computador mediante el cable USB.

El programa utiliza el puerto:

    COM3

### 2. Programar el ESP32

Abrir el archivo:

    baxter_esp32.ino

en Arduino IDE.

Seleccionar la placa:

    ESP32 Dev Module

Seleccionar el puerto correspondiente al ESP32 y cargar el programa.

### 3. Cerrar el monitor serial

Antes de ejecutar Python se debe cerrar el Monitor Serial de Arduino IDE para evitar que COM3 quede ocupado.

### 4. Ejecutar Python

Abrir una terminal en la carpeta:

    TALLER PUNTO 2

y ejecutar:

    py -3.12 baxter_esp32_control.py

Se abrirá la ventana de simulación de PyBullet con el robot Baxter.

---

## Controles

| Elemento | Función |
|---|---|
| Potenciómetro GPIO 34 | Control del brazo izquierdo |
| Potenciómetro GPIO 35 | Control del brazo derecho |
| Tecla 1 | Abrir pinzas |
| Tecla 2 | Cerrar pinzas y agarrar objeto |

---

## Archivos del proyecto

    TALLER PUNTO 2/
    │
    ├── baxter_esp32.ino
    │
    ├── baxter_esp32_control.py
    │
    ├── README.md
    │
    └── data/
        └── baxter_common/
            └── baxter_description/
                └── urdf/
                    └── toms_baxter.urdf

La carpeta `data` contiene los archivos necesarios para cargar correctamente el modelo Baxter y sus recursos dentro de PyBullet.

---

## Modelo de Baxter

El modelo utilizado en este proyecto está basado en el repositorio:

https://github.com/erwincoumans/pybullet_robots

Dentro del proyecto se utiliza el modelo:

    toms_baxter.urdf

Este archivo permite cargar el robot Baxter dentro de la simulación de PyBullet.

---

## Resultados

El sistema desarrollado permite integrar una consola física basada en ESP32 con una simulación robótica realizada en Python y PyBullet.

Se logró implementar:

- Lectura de dos potenciómetros mediante el ESP32.
- Comunicación serial entre ESP32 y Python.
- Control del brazo izquierdo mediante GPIO 34.
- Control del brazo derecho mediante GPIO 35.
- Control de apertura de las pinzas.
- Control de cierre de las pinzas.
- Creación de un objeto dentro de la simulación.
- Agarre del objeto.
- Movimiento del objeto mediante el robot Baxter.

El proyecto demuestra la integración entre sistemas embebidos, comunicación serial, simulación robótica y control de actuadores.

---

## Conclusión

El desarrollo permitió implementar una consola de mandos física utilizando un ESP32 para controlar un robot Baxter simulado en PyBullet.

Los dos potenciómetros permiten generar movimientos continuos para los brazos del robot, mientras que el teclado permite controlar las pinzas.

La integración con un objeto dentro de la simulación permite demostrar una aplicación básica de manipulación robótica, en la cual el robot puede agarrar y desplazar un objeto.

De esta manera se cumple el objetivo de desarrollar una interfaz de control para lograr movilidad y posicionamiento del robot, además de permitir la interacción con un objeto.

---

## Integrantes

**Ingeniería Mecatrónica**

**Universidad Militar Nueva Granada**

Proyecto desarrollado para el taller de Microcontroladores y Robótica.