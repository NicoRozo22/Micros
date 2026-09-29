# TALLER PUNTO 2 — CONTROL DE BRAZO ROBÓTICO BAXTER CON ESP32

## OBJETIVO

Desarrollar una aplicación de comunicación Real-to-Sim en la que un teclado matricial conectado a una ESP32 permita controlar un brazo robótico Baxter dentro de una simulación realizada en PyBullet.

El sistema permite realizar movimientos del brazo, posicionarlo frente a un objeto, realizar un agarre simulado y trasladar el objeto hacia otra posición.

## DESCRIPCIÓN DEL PROYECTO

Para esta práctica se utilizó como referencia el repositorio de robots para PyBullet:

https://github.com/erwincoumans/pybullet_robots

A partir del archivo baxter_ik_demo.py se desarrolló el programa baxter_esp32.py, incorporando comunicación serial con la ESP32.

La ESP32 recibe las teclas de un teclado matricial 4x4 y envía los comandos mediante comunicación serial al computador.

Python recibe estos comandos y controla el brazo robótico Baxter dentro del entorno de simulación PyBullet.

## FLUJO DEL SISTEMA

TECLADO MATRICIAL 4x4
        ↓
      ESP32
        ↓
COMUNICACIÓN SERIAL
        ↓
      PYTHON
        ↓
     PYBULLET
        ↓
   BRAZO BAXTER
        ↓
MOVIMIENTO / AGARRE / TRASLADO

## MATERIALES

- ESP32 Dev Module
- Teclado matricial 4x4
- Computador
- Cable USB para ESP32
- Python 3.12
- PyBullet
- PySerial
- Visual Studio Code
- Arduino IDE
- Git
- GitHub

## CONEXIÓN DEL TECLADO MATRICIAL

El teclado matricial 4x4 se conecta a la ESP32 de la siguiente manera:

R1 → GPIO 13
R2 → GPIO 14
R3 → GPIO 25
R4 → GPIO 26

C1 → GPIO 27
C2 → GPIO 32
C3 → GPIO 33
C4 → GPIO 16

La comunicación serial entre la ESP32 y Python se realiza a 115200 baudios.

## PROGRAMA DE LA ESP32

La ESP32 utiliza la librería Keypad para detectar las teclas del teclado matricial.

Cuando se presiona una tecla, la ESP32 envía el carácter correspondiente mediante comunicación serial.

El programa utilizado es:

#include <Keypad.h>

const byte FILAS = 4;
const byte COLUMNAS = 4;

char teclas[FILAS][COLUMNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte pinesFilas[FILAS] = {
  13, 14, 25, 26
};

byte pinesColumnas[COLUMNAS] = {
  27, 32, 33, 16
};

Keypad teclado = Keypad(
  makeKeymap(teclas),
  pinesFilas,
  pinesColumnas,
  FILAS,
  COLUMNAS
);

void setup() {
  Serial.begin(115200);
}

void loop() {
  char tecla = teclado.getKey();

  if (tecla) {
    Serial.write(tecla);
  }
}

## COMANDOS DEL SISTEMA

1 → Mover el brazo hacia arriba.

2 → Mover el brazo hacia abajo.

4 → Mover el brazo hacia la izquierda.

6 → Mover el brazo hacia la derecha.

8 → Mover el brazo hacia adelante.

5 → Mover el brazo hacia atrás.

A → Regresar a la posición inicial.

B → Posicionar el brazo frente al objeto.

C → Agarrar o liberar el objeto.

D → Levantar y trasladar el objeto.

X → Finalizar la simulación.

## FUNCIONAMIENTO DEL SISTEMA

### 1. INICIO DE LA SIMULACIÓN

Al ejecutar el programa baxter_esp32.py se abre el entorno de simulación de PyBullet.

En la escena aparecen el brazo robótico Baxter y un objeto azul que será manipulado por el brazo.

El objeto se encuentra visible desde el inicio de la simulación.

### 2. MOVIMIENTO MANUAL

Las teclas 1, 2, 4, 6, 8 y 5 permiten realizar movimientos manuales del brazo.

Cada tecla es detectada por la ESP32 y enviada al computador mediante comunicación serial.

Python interpreta el comando recibido y modifica la posición objetivo del brazo Baxter.

### 3. POSICIÓN INICIAL

La tecla A permite regresar el brazo a la posición inicial.

También permite restablecer la posición del objeto para realizar nuevamente la demostración.

### 4. POSICIONAMIENTO FRENTE AL OBJETO

La tecla B hace que el brazo se desplace hasta una posición cercana al objeto.

Esta posición permite preparar el brazo para realizar el agarre.

### 5. AGARRE DEL OBJETO

La tecla C activa o desactiva el estado de agarre.

Cuando el objeto se encuentra agarrado, su posición se actualiza de acuerdo con la posición del extremo del brazo.

De esta manera se simula la interacción entre el brazo y el objeto dentro del entorno virtual.

### 6. LEVANTAMIENTO Y TRASLADO

La tecla D realiza la secuencia de traslado.

Primero el brazo levanta el objeto y posteriormente se desplaza hacia una segunda posición dentro del entorno de PyBullet.

Mientras el objeto está agarrado, este acompaña el movimiento del brazo.

### 7. LIBERACIÓN

La tecla C puede utilizarse nuevamente para liberar el objeto.

Una vez liberado, el objeto deja de seguir al extremo del brazo.

### 8. FINALIZACIÓN

La tecla X finaliza el programa y cierra la simulación.

## SECUENCIA DE DEMOSTRACIÓN

Para realizar una demostración completa del funcionamiento se puede utilizar la siguiente secuencia:

A → Posición inicial.

B → Llevar el brazo hacia el objeto.

C → Agarrar el objeto.

D → Levantar y trasladar el objeto.

C → Liberar el objeto.

También es posible utilizar las teclas de movimiento manual:

1 → Arriba.

2 → Abajo.

4 → Izquierda.

6 → Derecha.

8 → Adelante.

5 → Atrás.

## COMUNICACIÓN REAL-TO-SIM

El proyecto implementa el concepto Real-to-Sim porque las acciones realizadas mediante un dispositivo físico, en este caso la ESP32 con el teclado matricial, controlan un elemento dentro de una simulación virtual.

La comunicación completa es:

USUARIO
↓
TECLADO MATRICIAL
↓
ESP32
↓
COMUNICACIÓN SERIAL
↓
PYTHON
↓
PYBULLET
↓
BRAZO ROBÓTICO BAXTER

## CONTROL DEL BRAZO MEDIANTE CINEMÁTICA INVERSA

El programa utiliza las funciones de PyBullet para calcular la posición de las articulaciones necesarias para alcanzar las posiciones objetivo.

La cinemática inversa permite determinar los movimientos de las articulaciones del brazo a partir de una posición objetivo del extremo del robot.

De esta forma, el usuario puede controlar la posición del brazo mediante comandos sencillos enviados desde la ESP32.

## OBJETO DE LA SIMULACIÓN

Dentro del entorno se utiliza un objeto de color azul para representar el elemento que será manipulado por el brazo Baxter.

El objeto se encuentra visible desde el comienzo de la simulación.

Durante el proceso de agarre, el programa actualiza su posición para simular que permanece sujeto al extremo del brazo.

## SOFTWARE UTILIZADO

- Python 3.12
- PyBullet
- PySerial
- Visual Studio Code
- Arduino IDE
- Git
- GitHub

## INSTALACIÓN Y CONFIGURACIÓN

Se utilizó Python 3.12 para ejecutar el programa.

Las principales librerías utilizadas son:

- PyBullet
- PySerial

El proyecto de Baxter utilizado como referencia corresponde al repositorio:

https://github.com/erwincoumans/pybullet_robots

## EJECUCIÓN DEL PROGRAMA

Primero se debe conectar la ESP32 al computador mediante USB.

Después se debe cargar el programa de la ESP32 utilizando Arduino IDE.

Es importante cerrar el Monitor Serial del Arduino IDE antes de ejecutar Python, ya que Python necesita utilizar el puerto serial de la ESP32.

El archivo principal de la simulación es:

baxter_esp32.py

Desde la terminal, ubicarse en la carpeta donde se encuentra el archivo y ejecutar:

py -3.12 baxter_esp32.py

Al ejecutar el programa se abrirá la simulación de PyBullet con el brazo Baxter y el objeto azul.

## ARCHIVOS DEL PROYECTO

TALLER PUNTO 2/

├── README.md

└── baxter_esp32.py

README.md

Este archivo contiene la documentación del proyecto, incluyendo:

- Objetivo.
- Materiales.
- Conexiones.
- Comandos.
- Funcionamiento.
- Comunicación Real-to-Sim.
- Ejecución.
- Resultado.

baxter_esp32.py

Es el programa principal desarrollado en Python para controlar el brazo Baxter mediante la ESP32.

## RESULTADO

Se logró implementar correctamente la comunicación entre el sistema físico y la simulación virtual.

El resultado final permite controlar el brazo Baxter mediante un teclado matricial conectado a la ESP32.

El sistema permite:

- Mover el brazo manualmente.
- Regresar a la posición inicial.
- Posicionar el brazo frente al objeto.
- Agarrar el objeto.
- Levantar el objeto.
- Trasladar el objeto.
- Liberar el objeto.
- Finalizar la simulación.

La arquitectura final del proyecto es:

ESP32
↓
Comunicación Serial
↓
Python
↓
PyBullet
↓
Baxter
↓
Manipulación del objeto

## EVIDENCIA DE FUNCIONAMIENTO

Durante las pruebas se verificó:

- Comunicación correcta entre ESP32 y Python.
- Movimiento del brazo Baxter mediante el teclado.
- Aparición del objeto desde el inicio.
- Posicionamiento del brazo frente al objeto.
- Agarre del objeto.
- Levantamiento del objeto.
- Traslado hacia una segunda posición.
- Liberación del objeto.
- Finalización de la simulación.

## AUTOR

Nicolás Rozo

Universidad Militar Nueva Granada

Ingeniería Mecatrónica