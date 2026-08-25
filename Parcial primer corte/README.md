# PARCIAL 1 — FIGURA CASA + ÁRBOL

### Implementación mediante ESP32 y osciloscopio en modo XY

Universidad Militar Nueva Granada

---

## 1. Descripción del proyecto

En este proyecto se realizó el diseño e implementación de una figura correspondiente a una casa acompañada de un árbol, utilizando una ESP32 y un osciloscopio digital configurado en modo XY.

La figura fue construida mediante coordenadas en los ejes X y Y. La ESP32 genera las señales correspondientes a cada eje mediante sus salidas DAC, mientras que el osciloscopio representa visualmente la trayectoria generada.

El objetivo fue comprobar experimentalmente cómo es posible generar una figura gráfica mediante señales eléctricas y visualizarla utilizando la representación XY de un osciloscopio.

---

## 2. Objetivo

Diseñar e implementar una figura de CASA + ÁRBOL mediante la generación de señales X-Y utilizando una ESP32 y visualizar el resultado en un osciloscopio configurado en modo XY.

---

## 3. Materiales y herramientas

| Elemento | Función |
|---|---|
| ESP32 | Generación de las señales X y Y |
| Osciloscopio Tektronix TBS 1102B-EDU | Visualización de la trayectoria |
| Arduino IDE | Programación de la ESP32 |
| Salidas DAC | Generación de los niveles analógicos |
| Cables de conexión | Conexión entre la ESP32 y el osciloscopio |

---

## 4. Funcionamiento del sistema

El sistema utiliza dos salidas DAC de la ESP32 para generar las coordenadas de la figura.

| Salida | Función |
|---|---|
| GPIO 25 | Coordenada X |
| GPIO 26 | Coordenada Y |

El funcionamiento general puede representarse de la siguiente manera:

```text
                    ESP32
                      |
              +-------+-------+
              |               |
           GPIO 25         GPIO 26
              |               |
              X               Y
              |               |
              +-------+-------+
                      |
                      v
                 OSCILOSCOPIO
                    MODO XY
                      |
                      v
                 CASA + ÁRBOL
---

## 5. Conversión de coordenadas

El programa utiliza coordenadas normalizadas para facilitar la construcción de la figura.

Debido a que las salidas DAC de la ESP32 trabajan con valores entre 0 y 255, las coordenadas deben convertirse antes de ser enviadas a las salidas analógicas.

La conversión utilizada permite transformar las coordenadas en el rango aproximado de -1 a 1 a valores adecuados para el DAC.

La correspondencia aproximada es:

| Coordenada | Valor DAC |
|---|---:|
| -1 | 0 |
| 0 | 128 |
| +1 | 255 |

De esta manera, las coordenadas utilizadas para construir la casa y el árbol pueden ser representadas mediante las señales X e Y.

---

## 6. Interpolación de la trayectoria

Para obtener líneas continuas en el osciloscopio se utiliza interpolación lineal entre los diferentes puntos de la figura.

La interpolación permite generar puntos intermedios entre una coordenada inicial y una coordenada final.

La función utilizada es:

void linea(float x1, float y1, float x2, float y2, int pasos = 80)

---

## 7. Generación de la figura

La figura está compuesta por diferentes segmentos correspondientes a la casa y al árbol.

Las coordenadas se organizan de manera que el osciloscopio pueda recorrer la trayectoria completa utilizando las señales X e Y.

La casa está formada por:

- Base rectangular.
- Paredes laterales.
- Techo triangular.
- Puerta.
- Ventanas.

El árbol está formado por:

- Tronco.
- Copa del árbol.

Cada elemento se representa mediante coordenadas que posteriormente son interpoladas para obtener una trayectoria continua.

---

## 8. Funcionamiento del programa

El programa ejecutado en la ESP32 realiza las siguientes etapas:

1. Inicializa las salidas DAC de la ESP32.
2. Define las coordenadas correspondientes a la casa y al árbol.
3. Convierte las coordenadas al rango correspondiente a las salidas DAC.
4. Interpola los puntos de cada segmento.
5. Envía las señales X e Y al osciloscopio.
6. El osciloscopio trabaja en modo XY para representar gráficamente la figura.
7. El proceso se repite continuamente para mantener la figura visible.

De esta manera, la ESP32 funciona como generadora de las señales analógicas que permiten controlar la posición del punto mostrado por el osciloscopio.

---

## 9. Configuración del osciloscopio

Para visualizar correctamente la figura se utiliza el osciloscopio en modo XY.

La configuración utilizada es:

- Canal X: conectado a una salida DAC de la ESP32.
- Canal Y: conectado a la segunda salida DAC.
- Modo de visualización: XY.
- Escala vertical: ajustada para visualizar toda la figura.
- Escala horizontal: ajustada para obtener las proporciones adecuadas.

El modo XY permite utilizar directamente una señal para controlar la posición horizontal y otra para controlar la posición vertical del punto en pantalla.

---

## 10. Conexiones

Las conexiones principales del montaje son:

| Elemento | ESP32 |
|---|---|
| Señal X | DAC |
| Señal Y | DAC |
| GND del osciloscopio | GND |
| GND de la ESP32 | GND |

Las tierras de la ESP32 y del osciloscopio deben estar conectadas para establecer una referencia común entre las señales.

---

## 11. Resultado

El resultado obtenido corresponde a la representación de una figura formada por una casa acompañada de un árbol.

La figura se visualiza utilizando el osciloscopio en modo XY, demostrando que es posible generar diferentes formas geométricas mediante señales eléctricas generadas por la ESP32.

La trayectoria se mantiene mediante la generación continua de los puntos correspondientes a las coordenadas de la figura.

---

## 12. Conclusiones

Se logró implementar una figura gráfica utilizando una ESP32 y un osciloscopio configurado en modo XY.

El desarrollo permitió comprender la relación existente entre las coordenadas X-Y y las señales analógicas utilizadas para controlar la posición del punto en el osciloscopio.

También se comprobó la utilidad de la interpolación lineal para generar trayectorias continuas entre diferentes puntos.

Finalmente, se demostró que mediante la programación de las salidas DAC de la ESP32 es posible generar señales capaces de producir representaciones gráficas en un osciloscopio.

## 14. Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `oscilloscope_simple.ino` | Código fuente utilizado en la ESP32 |
| `README.md` | Documentación del proyecto |

