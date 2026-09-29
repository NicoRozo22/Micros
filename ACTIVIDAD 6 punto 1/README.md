# ACTIVIDAD 6 - PUNTO 1
## Teclado I2C + Simulación de brazo robótico en PyBullet

### Objetivo

Desarrollar un sistema de control de un brazo robótico mediante un teclado matricial 4x4 conectado a un ESP32. La información de las teclas se envía desde el ESP32 al computador mediante comunicación serial y se utiliza en Python para controlar un brazo robótico simulado en PyBullet.

El sistema permite seleccionar un dígito mediante el teclado y hacer que el brazo robótico trace la forma correspondiente en el espacio de trabajo de la simulación.

### Funcionamiento

El sistema funciona de la siguiente manera:

Teclado 4x4 → ESP32 → Comunicación Serial → Python → PyBullet → Brazo robótico

Al presionar un número del teclado, el ESP32 envía el carácter correspondiente por comunicación serial al computador.

El programa desarrollado en Python recibe el número y ejecuta una trayectoria previamente definida mediante puntos coordenados. El brazo robótico sigue estos puntos para dibujar el número seleccionado.

### Números disponibles

- 0 → Dibuja el número 0
- 1 → Dibuja el número 1
- 2 → Dibuja el número 2
- 3 → Dibuja el número 3
- 4 → Dibuja el número 4
- 5 → Dibuja el número 5
- 6 → Dibuja el número 6
- 7 → Dibuja el número 7
- 8 → Dibuja el número 8
- 9 → Dibuja el número 9
- D → Regresa el brazo a la posición inicial

### Materiales utilizados

- 1 ESP32 Dev Module
- 1 teclado matricial 4x4
- Cables Dupont
- Computador
- Software Arduino IDE
- Python 3.12
- PyBullet

### Conexiones del teclado

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

### Comunicación

La comunicación entre el ESP32 y el computador se realiza mediante comunicación serial a una velocidad de 115200 baudios.

El programa en Python recibe los caracteres enviados por el ESP32 y los interpreta para seleccionar la trayectoria correspondiente.

### Simulación del brazo

El brazo robótico se encuentra definido mediante el archivo `brazo.urdf`.

La simulación se ejecuta utilizando PyBullet y permite controlar las articulaciones del brazo mediante comandos de posición.

Para realizar los dibujos se utilizan coordenadas en los ejes X y Z. El programa convierte estas coordenadas en posiciones de las articulaciones del brazo y genera una trayectoria continua.

### Archivos

- `brazo.urdf`: modelo del brazo robótico utilizado en PyBullet.
- `main_control_dibujo.py`: programa principal que recibe los números desde el ESP32 y controla el brazo para realizar los dibujos.

### Ejecución

Primero se debe cargar en el ESP32 el programa del teclado y cerrar el Monitor Serial.

Después, desde la carpeta donde se encuentran los archivos del proyecto, se ejecuta:

```bash
py -3.12 main_control_dibujo.py

Al iniciar el programa se abre la simulación de PyBullet. Posteriormente se puede presionar cualquier número del teclado para que el brazo realice el dibujo correspondiente.

Resultado

Se obtuvo un sistema funcional en el que un teclado matricial conectado a un ESP32 permite seleccionar un número y enviar la información al computador. El programa en Python interpreta el número y controla un brazo robótico simulado en PyBullet para realizar la trayectoria correspondiente.
