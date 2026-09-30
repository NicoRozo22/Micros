import cv2
import mediapipe as mp
import serial
import time
import os
import math


# ============================================================
# ACTIVIDAD 4
# CONTROL DE ILUMINACION MEDIANTE GESTOS
# ESP32 + MEDIAPIPE + PYTHON
# ============================================================


# ============================================================
# CONFIGURACION
# ============================================================

PUERTO = "COM3"
BAUDRATE = 115200

MODELO = "gesture_recognizer.task"

TIEMPO_ENTRE_COMANDOS = 0.5


# ============================================================
# VERIFICAR MODELO
# ============================================================

if not os.path.exists(MODELO):

    print()
    print("ERROR: No se encontro gesture_recognizer.task")
    print()

    input("Presiona ENTER para cerrar...")
    exit()


# ============================================================
# CONECTAR ESP32
# ============================================================

print()
print("==============================================")
print(" ACTIVIDAD 4 - CONTROL POR GESTOS")
print("==============================================")
print()

print("Conectando ESP32 en", PUERTO, "...")

try:

    arduino = serial.Serial(
        PUERTO,
        BAUDRATE,
        timeout=0.1
    )

    time.sleep(2)

    arduino.reset_input_buffer()

    print("ESP32 conectada correctamente.")

except Exception as error:

    print()
    print("ERROR AL CONECTAR LA ESP32:")
    print(error)
    print()

    input("Presiona ENTER para cerrar...")
    exit()


# ============================================================
# CONFIGURAR MEDIAPIPE
# ============================================================

mp_tasks = mp.tasks
mp_vision = mp.tasks.vision


opciones = mp_vision.GestureRecognizerOptions(

    base_options=mp_tasks.BaseOptions(
        model_asset_path=MODELO
    ),

    running_mode=mp_vision.RunningMode.IMAGE,

    num_hands=1,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5
)


reconocedor = (
    mp_vision.GestureRecognizer
    .create_from_options(opciones)
)


# ============================================================
# ABRIR CAMARA
# ============================================================

camara = cv2.VideoCapture(0)


if not camara.isOpened():

    print()
    print("ERROR: No se pudo abrir la camara.")
    print()

    arduino.close()
    reconocedor.close()

    input("Presiona ENTER para cerrar...")
    exit()


# ============================================================
# FUNCION PARA CALCULAR DISTANCIA
# ============================================================

def distancia(p1, p2):

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z

    return math.sqrt(
        dx * dx +
        dy * dy +
        dz * dz
    )


# ============================================================
# DETECTAR GESTO VICTORY
#
# INDICE Y MEDIO EXTENDIDOS
# ANULAR Y MENIQUE DOBLADOS
# ============================================================

def detectar_victory(puntos):

    # Puntos de referencia
    muñeca = puntos[0]

    indice_mcp = puntos[5]
    indice_pip = puntos[6]
    indice_tip = puntos[8]

    medio_mcp = puntos[9]
    medio_pip = puntos[10]
    medio_tip = puntos[12]

    anular_mcp = puntos[13]
    anular_pip = puntos[14]
    anular_tip = puntos[16]

    menique_mcp = puntos[17]
    menique_pip = puntos[18]
    menique_tip = puntos[20]


    # --------------------------------------------------------
    # INDICE EXTENDIDO
    # --------------------------------------------------------

    indice_extendido = (
        distancia(muñeca, indice_tip)
        >
        distancia(muñeca, indice_pip) * 1.15
    )


    # --------------------------------------------------------
    # MEDIO EXTENDIDO
    # --------------------------------------------------------

    medio_extendido = (
        distancia(muñeca, medio_tip)
        >
        distancia(muñeca, medio_pip) * 1.15
    )


    # --------------------------------------------------------
    # ANULAR DOBLADO
    # --------------------------------------------------------

    anular_doblado = (
        distancia(muñeca, anular_tip)
        <
        distancia(muñeca, anular_pip) * 1.15
    )


    # --------------------------------------------------------
    # MENIQUE DOBLADO
    # --------------------------------------------------------

    menique_doblado = (
        distancia(muñeca, menique_tip)
        <
        distancia(muñeca, menique_pip) * 1.15
    )


    # --------------------------------------------------------
    # SEPARACION ENTRE INDICE Y MEDIO
    # --------------------------------------------------------

    separacion = distancia(
        indice_tip,
        medio_tip
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    if (

        indice_extendido
        and
        medio_extendido
        and
        anular_doblado
        and
        menique_doblado
        and
        separacion > 0.03

    ):

        return True


    return False


# ============================================================
# VARIABLES
# ============================================================

ultimo_comando = ""

ultimo_envio = 0


# ============================================================
# INFORMACION
# ============================================================

print()
print("==============================================")
print(" GESTOS DISPONIBLES")
print("==============================================")
print()

print("PUÑO          -> VERDE 1 -> 30%")
print("DOS DEDOS     -> VERDE 2 -> 70%")
print("MANO ABIERTA  -> ROJO    -> 100%")
print("PULGAR ABAJO  -> MODO 1")
print("PULGAR ARRIBA -> MODO 2")

print()

print("Presiona Q para salir.")

print()
print("==============================================")
print()


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # LEER CAMARA
        # ----------------------------------------------------

        correcto, frame = camara.read()


        if not correcto:

            print("No se pudo leer la camara.")

            break


        # ----------------------------------------------------
        # ESPEJO
        # ----------------------------------------------------

        frame = cv2.flip(frame, 1)


        # ----------------------------------------------------
        # CONVERTIR A RGB
        # ----------------------------------------------------

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # ----------------------------------------------------
        # CREAR IMAGEN MEDIAPIPE
        # ----------------------------------------------------

        imagen_mp = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )


        # ----------------------------------------------------
        # RECONOCER
        # ----------------------------------------------------

        resultado = reconocedor.recognize(
            imagen_mp
        )


        gesto = "NINGUNO"

        confianza = 0.0


        # ====================================================
        # OBTENER RESULTADO DEL CLASIFICADOR
        # ====================================================

        if resultado.gestures:

            if len(resultado.gestures[0]) > 0:

                gesto = (
                    resultado
                    .gestures[0][0]
                    .category_name
                )

                confianza = (
                    resultado
                    .gestures[0][0]
                    .score
                )


        # ====================================================
        # CORRECCION ESPECIAL PARA VICTORY
        # ====================================================

        victory_detectado = False


        if resultado.hand_landmarks:

            if len(resultado.hand_landmarks) > 0:

                puntos = resultado.hand_landmarks[0]

                victory_detectado = detectar_victory(
                    puntos
                )


        # Si la geometria de la mano indica V,
        # damos prioridad a Victory.

        if victory_detectado:

            gesto = "Victory"

            confianza = max(
                confianza,
                0.90
            )


        # ====================================================
        # MOSTRAR RESULTADO
        # ====================================================

        texto = (
            f"Gesto: {gesto} | "
            f"Confianza: {confianza:.2f}"
        )


        cv2.putText(

            frame,

            texto,

            (20, 45),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2
        )


        # ====================================================
        # DETERMINAR COMANDO
        # ====================================================

        comando = None


        # ----------------------------------------------------
        # PUÑO
        # ----------------------------------------------------

        if gesto == "Closed_Fist":

            comando = "FIST"


        # ----------------------------------------------------
        # DOS DEDOS
        # ----------------------------------------------------

        elif gesto == "Victory":

            comando = "VICTORY"


        # ----------------------------------------------------
        # MANO ABIERTA
        # ----------------------------------------------------

        elif gesto == "Open_Palm":

            comando = "OPEN"


        # ----------------------------------------------------
        # PULGAR ABAJO
        # ----------------------------------------------------

        elif gesto == "Thumb_Down":

            comando = "MODE1"


        # ----------------------------------------------------
        # PULGAR ARRIBA
        # ----------------------------------------------------

        elif gesto == "Thumb_Up":

            comando = "MODE2"


        # ====================================================
        # ENVIAR COMANDO
        # ====================================================

        ahora = time.time()


        if comando is not None:

            if (

                comando != ultimo_comando

                and

                ahora - ultimo_envio
                >= TIEMPO_ENTRE_COMANDOS

            ):

                arduino.write(
                    (
                        comando + "\n"
                    ).encode()
                )


                print(
                    "Gesto:",
                    gesto,
                    "| Confianza:",
                    round(confianza, 2),
                    "| Comando:",
                    comando
                )


                ultimo_comando = comando

                ultimo_envio = ahora


        # ----------------------------------------------------
        # SIN GESTO
        # ----------------------------------------------------

        elif gesto == "NINGUNO":

            ultimo_comando = ""


        # ====================================================
        # MOSTRAR CAMARA
        # ====================================================

        cv2.imshow(
            "Actividad 4 - Control por Gestos",
            frame
        )


        # ====================================================
        # SALIR
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


# ============================================================
# CTRL + C
# ============================================================

except KeyboardInterrupt:

    print()
    print("Programa detenido por el usuario.")


# ============================================================
# CERRAR TODO
# ============================================================

finally:

    print()
    print("Cerrando conexiones...")


    try:

        arduino.write(
            b"OFF\n"
        )

        time.sleep(0.2)

    except:

        pass


    try:

        arduino.close()

    except:

        pass


    try:

        camara.release()

    except:

        pass


    try:

        cv2.destroyAllWindows()

    except:

        pass


    try:

        reconocedor.close()

    except:

        pass


    print("Programa finalizado.")