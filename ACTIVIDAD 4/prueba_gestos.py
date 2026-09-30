import cv2
import mediapipe as mp
import urllib.request
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

MODELO = "gesture_recognizer.task"

URL_MODELO = (
    "https://storage.googleapis.com/mediapipe-models/"
    "gesture_recognizer/gesture_recognizer/float16/1/"
    "gesture_recognizer.task"
)

# ============================================================
# DESCARGAR MODELO SI NO EXISTE
# ============================================================

if not os.path.exists(MODELO):
    print("Descargando modelo de MediaPipe...")
    urllib.request.urlretrieve(URL_MODELO, MODELO)
    print("Modelo descargado correctamente.")

# ============================================================
# MEDIA PIPE
# ============================================================

mp_tasks = mp.tasks
mp_vision = mp.tasks.vision

opciones = mp_vision.GestureRecognizerOptions(
    base_options=mp_tasks.BaseOptions(
        model_asset_path=MODELO
    ),
    running_mode=mp_vision.RunningMode.IMAGE
)

reconocedor = mp_vision.GestureRecognizer.create_from_options(
    opciones
)

# ============================================================
# CÁMARA
# ============================================================

camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print()
print("======================================")
print("   PRUEBA DE RECONOCIMIENTO DE MANO")
print("======================================")
print()
print("Coloca tu mano frente a la cámara.")
print()
print("Gestos que vamos a probar:")
print("Closed_Fist   = Puño")
print("Pointing_Up   = Un dedo")
print("Open_Palm     = Mano abierta")
print("Thumb_Down    = Pulgar abajo")
print("Thumb_Up      = Pulgar arriba")
print()
print("Presiona Q para salir.")
print()

# ============================================================
# BUCLE
# ============================================================

while True:

    correcto, frame = camara.read()

    if not correcto:
        print("No se pudo leer la cámara.")
        break

    # Voltear imagen como espejo
    frame = cv2.flip(frame, 1)

    # Convertir BGR a RGB
    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Convertir imagen para MediaPipe
    imagen_mp = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb
    )

    # Reconocer gesto
    resultado = reconocedor.recognize(imagen_mp)

    gesto = "NINGUNO"
    confianza = 0.0

    if resultado.gestures:

        if len(resultado.gestures[0]) > 0:

            gesto = resultado.gestures[0][0].category_name

            confianza = (
                resultado.gestures[0][0].score
            )

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    texto = f"{gesto}  {confianza:.2f}"

    cv2.putText(
        frame,
        texto,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Reconocimiento de gestos - Actividad 4",
        frame
    )

    # Mostrar gesto también en terminal
    if gesto != "None":
        print(
            f"Gesto: {gesto} | "
            f"Confianza: {confianza:.2f}"
        )

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ============================================================
# CERRAR
# ============================================================

camara.release()
cv2.destroyAllWindows()
reconocedor.close()

print()
print("Programa finalizado.")