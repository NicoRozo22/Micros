# TALLER PUNTO 3 — CONSOLA DE MANDOS ESP32 PARA MOVIMIENTO FLUIDO DEL ROBOT BAXTER

## OBJETIVO

Desarrollar una consola de mandos utilizando una ESP32 y un teclado matricial 4x4 para controlar de manera fluida el movimiento de un robot Baxter dentro de un entorno de simulación realizado con PyBullet.

El objetivo principal es permitir una movilidad más continua y natural del brazo robótico, utilizando comandos enviados desde la ESP32 hacia un programa desarrollado en Python.

## REPOSITORIO DE REFERENCIA

El proyecto se desarrolló tomando como referencia el repositorio proporcionado por el docente:

https://github.com/erwincoumans/pybullet_robots/tree/master

Dentro de este repositorio se utilizó como referencia el programa de demostración del robot Baxter y su sistema de cinemática inversa.

## DESCRIPCIÓN DEL PROYECTO

El sistema está compuesto por una ESP32, un teclado matricial 4x4, un computador y el entorno de simulación PyBullet.

El usuario presiona una tecla en el teclado conectado a la ESP32.

La ESP32 identifica la tecla y la envía mediante comunicación serial al computador.

El programa desarrollado en Python recibe el comando y modifica progresivamente la posición objetivo del brazo Baxter.

A diferencia de un movimiento basado únicamente en posiciones fijas, el programa implementa una modificación gradual de la posición objetivo, permitiendo que el movimiento del brazo sea más fluido.

## ARQUITECTURA DEL SISTEMA

USUARIO
↓
TECLADO MATRICIAL 4x4
↓
ESP32
↓
COMUNICACIÓN SERIAL
↓
PYTHON
↓
CINEMÁTICA INVERSA
↓
CONTROL DE ARTICULACIONES
↓
PYBULLET
↓
ROBOT BAXTER

## COMPONENTES

- ESP32 Dev Module
- Teclado matricial 4x4
- Computador
- Cable USB
- Python 3.12
- PyBullet
- PySerial
- Visual Studio Code
- Arduino IDE
- Git
- GitHub

## CONEXIÓN DEL TECLADO

La conexión utilizada para el teclado matricial 4x4 es:

R1 → GPIO 13
R2 → GPIO 14
R3 → GPIO 25
R4 → GPIO 26

C1 → GPIO 27
C2 → GPIO 32
C3 → GPIO 33
C4 → GPIO 16

La comunicación serial utilizada entre la ESP32 y Python es de:

115200 baudios

## CONSOLA DE MANDOS

La consola utiliza las siguientes teclas:

1 → Movimiento hacia arriba.

2 → Movimiento hacia abajo.

4 → Movimiento hacia la izquierda.

6 → Movimiento hacia la derecha.

8 → Movimiento hacia adelante.

5 → Movimiento hacia atrás.

A → Regresar a la posición inicial.

0 → Detener el movimiento.

X → Finalizar la simulación.

## FUNCIONAMIENTO DE LOS MOVIMIENTOS

### MOVIMIENTO HACIA ARRIBA

Al recibir el comando 1, el programa incrementa progresivamente la coordenada vertical del objetivo del brazo.

Esto permite que el brazo se desplace hacia arriba de manera gradual.

### MOVIMIENTO HACIA ABAJO

Al recibir el comando 2, el programa disminuye progresivamente la coordenada vertical del objetivo.

El movimiento se realiza de manera gradual para evitar cambios bruscos.

### MOVIMIENTO HACIA LA IZQUIERDA

La tecla 4 modifica progresivamente la coordenada horizontal del objetivo hacia la izquierda.

### MOVIMIENTO HACIA LA DERECHA

La tecla 6 modifica progresivamente la coordenada horizontal del objetivo hacia la derecha.

### MOVIMIENTO HACIA ADELANTE

La tecla 8 modifica progresivamente la coordenada correspondiente al desplazamiento hacia adelante.

### MOVIMIENTO HACIA ATRÁS

La tecla 5 modifica progresivamente la coordenada correspondiente al desplazamiento hacia atrás.

### DETENER MOVIMIENTO

La tecla 0 establece el comando de movimiento en estado de detención.

Esto permite mantener el brazo en la posición alcanzada.

### POSICIÓN INICIAL

La tecla A permite regresar el brazo a una posición inicial previamente establecida.

### FINALIZAR

La tecla X finaliza la ejecución del programa y cierra la comunicación con la ESP32 y la simulación de PyBullet.

## MOVIMIENTO FLUIDO

Para conseguir un movimiento más fluido, el programa no lleva directamente el brazo desde la posición actual hasta la posición final.

En lugar de esto, calcula progresivamente una nueva posición intermedia.

La posición actual se aproxima continuamente a la posición objetivo.

Este procedimiento permite reducir los cambios bruscos de posición y proporciona un desplazamiento más suave del brazo Baxter.

## CINEMÁTICA INVERSA

El programa utiliza la función de cinemática inversa disponible en PyBullet.

La cinemática inversa permite determinar las posiciones de las articulaciones necesarias para que el extremo del brazo alcance una determinada posición en el espacio.

El proceso general es:

POSICIÓN OBJETIVO
↓
CINEMÁTICA INVERSA
↓
POSICIONES DE ARTICULACIONES
↓
CONTROL DE MOTORES
↓
MOVIMIENTO DEL BAXTER

## CONTROL DE ARTICULACIONES

Una vez calculadas las posiciones mediante cinemática inversa, el programa utiliza el control de posición de PyBullet para llevar las articulaciones hacia los valores calculados.

El movimiento se actualiza continuamente durante la simulación.

## LIMITES DE MOVIMIENTO

El programa incorpora límites para las coordenadas de movimiento del brazo.

Estos límites evitan que el objetivo se desplace indefinidamente y ayudan a mantener el movimiento dentro de una zona determinada de la simulación.

## COMUNICACIÓN ESP32 — PYTHON

La comunicación entre la ESP32 y Python se realiza mediante el puerto serial.

La ESP32 detecta la tecla presionada y transmite el carácter correspondiente.

Python recibe el carácter y lo utiliza como comando de control.

El proceso es:

TECLA
↓
ESP32
↓
SERIAL
↓
PYTHON
↓
COMANDO
↓
POSICIÓN OBJETIVO
↓
CINEMÁTICA INVERSA
↓
BAXTER

## PROGRAMA DE LA ESP32

La ESP32 utiliza la librería Keypad para identificar las teclas del teclado matricial.

El programa envía únicamente el carácter correspondiente a la tecla presionada mediante Serial.write.

La velocidad de comunicación utilizada es de 115200 baudios.

## PROGRAMA PRINCIPAL

El archivo principal de este punto es:

baxter_esp32_fluido.py

Este programa contiene:

- Configuración de la comunicación serial.
- Inicialización de PyBullet.
- Carga del robot Baxter.
- Configuración de la cinemática inversa.
- Posición inicial.
- Lectura de comandos de la ESP32.
- Movimiento progresivo.
- Límites de seguridad.
- Control de las articulaciones.
- Finalización de la simulación.

## SOFTWARE UTILIZADO

- Python 3.12
- PyBullet
- PySerial
- Arduino IDE
- Visual Studio Code
- Git
- GitHub

## EJECUCIÓN DEL PROGRAMA

Para ejecutar el programa es necesario conectar primero la ESP32 al computador.

El Monitor Serial de Arduino IDE debe permanecer cerrado mientras Python utiliza el puerto de la ESP32.

El programa se ejecuta desde la carpeta del repositorio de PyBullet, debido a que allí se encuentran los archivos y modelos necesarios para cargar el robot Baxter.

El comando utilizado es:

py -3.12 baxter_esp32_fluido.py

Al ejecutar el programa se abre la ventana de PyBullet y aparece el robot Baxter.

## PRUEBA DE FUNCIONAMIENTO

Para realizar una prueba del sistema se puede utilizar la siguiente secuencia:

1. Conectar la ESP32 al computador.
2. Cerrar el Monitor Serial de Arduino IDE.
3. Ejecutar baxter_esp32_fluido.py.
4. Esperar a que aparezca la simulación de Baxter.
5. Presionar 1 para mover el brazo hacia arriba.
6. Presionar 2 para moverlo hacia abajo.
7. Presionar 4 para moverlo hacia la izquierda.
8. Presionar 6 para moverlo hacia la derecha.
9. Presionar 8 para moverlo hacia adelante.
10. Presionar 5 para moverlo hacia atrás.
11. Presionar 0 para detener el movimiento.
12. Presionar A para regresar a la posición inicial.
13. Presionar X para finalizar la simulación.

## RESULTADOS

Se desarrolló una consola de mandos física utilizando una ESP32 y un teclado matricial.

La consola permite enviar comandos desde el sistema físico hacia una simulación del robot Baxter.

El programa desarrollado permite realizar movimientos progresivos en diferentes direcciones.

Se implementó un mecanismo de suavizado mediante aproximación progresiva de la posición actual hacia la posición objetivo.

Esto permite obtener un movimiento más continuo del robot dentro del entorno virtual.

## RESULTADO FINAL

La comunicación implementada es:

ESP32 → Comunicación Serial → Python → PyBullet → Baxter

El sistema permite utilizar una consola física para controlar el movimiento del robot Baxter dentro de un entorno virtual.

## ARCHIVOS DEL PROYECTO

TALLER PUNTO 3/

├── README.md

└── baxter_esp32_fluido.py

## EVIDENCIAS

Para la entrega del proyecto se pueden incluir evidencias del funcionamiento del sistema, tales como:

- Fotografía de la ESP32 conectada al teclado.
- Fotografía del montaje físico.
- Captura de la consola de Python.
- Captura del robot Baxter en PyBullet.
- Video del movimiento del robot.
- Video mostrando los diferentes comandos de la consola.

## VIDEO DE FUNCIONAMIENTO

Se recomienda realizar un video mostrando:

1. El montaje de la ESP32 y el teclado.
2. La conexión del sistema.
3. La ejecución del programa.
4. El movimiento hacia arriba.
5. El movimiento hacia abajo.
6. El movimiento hacia izquierda y derecha.
7. El movimiento hacia adelante y atrás.
8. La detención.
9. El regreso a la posición inicial.

## CONCLUSIÓN

Se desarrolló una consola de mandos basada en ESP32 para controlar un robot Baxter simulado en PyBullet.

La comunicación serial permitió conectar el sistema físico con el entorno virtual.

Mediante cinemática inversa y control progresivo de la posición objetivo se consiguió un movimiento más fluido del brazo.

El proyecto demuestra la integración entre hardware, programación, comunicación serial, cinemática inversa y simulación robótica.

## AUTOR

Nicolás Rozo

Universidad Militar Nueva Granada

Ingeniería Mecatrónica