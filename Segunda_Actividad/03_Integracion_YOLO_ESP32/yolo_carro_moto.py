from ultralytics import YOLO
import cv2
import serial
import time

# ==============================
# CONFIGURACIÓN
# ==============================

PUERTO_ESP32 = "COM3"
VELOCIDAD = 115200

# Cargar modelo YOLO
modelo = YOLO("yolo11n.pt")

# Conectar con ESP32
esp32 = serial.Serial(PUERTO_ESP32, VELOCIDAD, timeout=1)
time.sleep(2)

print("ESP32 conectado correctamente")

# Abrir cámara
camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("No se pudo abrir la cámara")
    esp32.close()
    exit()

# ==============================
# PROGRAMA PRINCIPAL
# ==============================

while True:

    ret, frame = camara.read()

    if not ret:
        print("No se pudo leer la cámara")
        break

    # Ejecutar YOLO
    resultados = modelo(frame, verbose=False)

    objeto = "NINGUNO"

    # Revisar objetos detectados
    for resultado in resultados:

        for caja in resultado.boxes:

            clase = int(caja.cls[0])
            confianza = float(caja.conf[0])

            x1, y1, x2, y2 = map(int, caja.xyxy[0])

            # ==============================
            # CARRO
            # ==============================

            if clase == 2 and confianza >= 0.50:

                objeto = "CARRO"

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"CARRO {confianza:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            # ==============================
            # MOTO
            # ==============================

            elif clase == 3 and confianza >= 0.50:

                objeto = "MOTO"

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"MOTO {confianza:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2
                )

    # ==============================
    # ENVIAR AL ESP32
    # ==============================

    esp32.write((objeto + "\n").encode())

    print("Detectado:", objeto)

    # Mostrar estado
    cv2.putText(
        frame,
        f"OBJETO: {objeto}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        3
    )

    cv2.imshow("YOLO - CARRO Y MOTO", frame)

    # Presionar Q para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ==============================
# FINALIZAR
# ==============================

camara.release()
esp32.close()
cv2.destroyAllWindows()