import time
import serial
import pybullet as p
import pybullet_data
import numpy as np


# ============================================================
# CONFIGURACIÓN
# ============================================================

PUERTO_ESP32 = "COM3"
BAUDRATE = 115200

# Extremo del brazo Baxter utilizado por el demo original
END_EFFECTOR_ID = 48

# Velocidad del movimiento
VELOCIDAD = 0.004

# Incremento máximo permitido por movimiento
PASO_MAXIMO = 0.008


# ============================================================
# CONFIGURAR EL MUNDO
# ============================================================

def setUpWorld(initialSimSteps=100):

    p.resetSimulation()

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Plano
    p.loadURDF(
        "plane.urdf",
        [0, 0, -1],
        useFixedBase=True
    )

    # Baxter
    baxterId = p.loadURDF(
        "baxter_common/baxter_description/urdf/toms_baxter.urdf",
        useFixedBase=True
    )

    p.resetBasePositionAndOrientation(
        baxterId,
        [0.5, -0.8, 0.0],
        [0., 0., -1., -1.]
    )

    p.setGravity(0, 0, -10)

    for _ in range(initialSimSteps):
        p.stepSimulation()

    return baxterId


# ============================================================
# RANGOS DE LAS ARTICULACIONES
# ============================================================

def getJointRanges(bodyId):

    lowerLimits = []
    upperLimits = []
    jointRanges = []
    restPoses = []

    numJoints = p.getNumJoints(bodyId)

    for i in range(numJoints):

        jointInfo = p.getJointInfo(bodyId, i)

        if jointInfo[3] > -1:

            lowerLimits.append(-2)
            upperLimits.append(2)
            jointRanges.append(2)

            restPoses.append(
                p.getJointState(bodyId, i)[0]
            )

    return (
        lowerLimits,
        upperLimits,
        jointRanges,
        restPoses
    )


# ============================================================
# CINEMÁTICA INVERSA
# ============================================================

def calcular_IK(
    baxterId,
    targetPosition,
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses
):

    jointPoses = p.calculateInverseKinematics(
        baxterId,
        END_EFFECTOR_ID,
        targetPosition,
        lowerLimits=lowerLimits,
        upperLimits=upperLimits,
        jointRanges=jointRanges,
        restPoses=restPoses
    )

    return jointPoses


# ============================================================
# MOVER ARTICULACIONES
# ============================================================

def mover_brazo(
    baxterId,
    jointPoses
):

    numJoints = p.getNumJoints(baxterId)

    for i in range(numJoints):

        jointInfo = p.getJointInfo(
            baxterId,
            i
        )

        qIndex = jointInfo[3]

        if qIndex > -1:

            indice = qIndex - 7

            if 0 <= indice < len(jointPoses):

                p.setJointMotorControl2(
                    bodyIndex=baxterId,
                    jointIndex=i,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=jointPoses[indice],
                    force=500
                )


# ============================================================
# MOVIMIENTO SUAVE DEL OBJETIVO
# ============================================================

def mover_suave(
    posicion_actual,
    posicion_objetivo
):

    nueva_posicion = []

    for i in range(3):

        diferencia = (
            posicion_objetivo[i]
            - posicion_actual[i]
        )

        paso = diferencia * 0.15

        paso = max(
            -PASO_MAXIMO,
            min(PASO_MAXIMO, paso)
        )

        nueva_posicion.append(
            posicion_actual[i] + paso
        )

    return nueva_posicion


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("========================================")
    print(" BAXTER - CONSOLA ESP32")
    print(" MOVIMIENTO FLUIDO")
    print("========================================")

    print("Conectando con ESP32 en", PUERTO_ESP32)

    try:

        esp32 = serial.Serial(
            PUERTO_ESP32,
            BAUDRATE,
            timeout=0.01
        )

        time.sleep(2)

        print("ESP32 conectada correctamente.")

    except Exception as e:

        print("ERROR AL CONECTAR LA ESP32:")
        print(e)
        return


    # --------------------------------------------------------
    # PYBULLET
    # --------------------------------------------------------

    print("Iniciando PyBullet...")

    physicsClient = p.connect(p.GUI)

    if physicsClient < 0:

        print("No se pudo abrir PyBullet.")
        esp32.close()
        return


    p.resetDebugVisualizerCamera(
        cameraDistance=2.0,
        cameraYaw=180,
        cameraPitch=0,
        cameraTargetPosition=[0.52, 0.2, np.pi / 4]
    )


    # --------------------------------------------------------
    # BAXTER
    # --------------------------------------------------------

    baxterId = setUpWorld()

    lowerLimits, upperLimits, jointRanges, restPoses = \
        getJointRanges(baxterId)


    # --------------------------------------------------------
    # POSICIÓN INICIAL
    # --------------------------------------------------------

    posicion_inicial = [
        0.2,
        0.0,
        -0.1
    ]

    posicion_actual = posicion_inicial.copy()

    posicion_objetivo = posicion_inicial.copy()


    # --------------------------------------------------------
    # TEXTO EN LA SIMULACIÓN
    # --------------------------------------------------------

    p.addUserDebugText(
        "CONSOLA ESP32 - BAXTER",
        [0.2, 0.2, 0.4],
        textColorRGB=[1, 1, 1],
        textSize=1.5
    )

    p.addUserDebugText(
        "1/2 = ARRIBA / ABAJO",
        [0.2, 0.2, 0.3],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )

    p.addUserDebugText(
        "4/6 = IZQUIERDA / DERECHA",
        [0.2, 0.2, 0.2],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )

    p.addUserDebugText(
        "8/5 = ADELANTE / ATRAS",
        [0.2, 0.2, 0.1],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )

    p.addUserDebugText(
        "0 = DETENER",
        [0.2, 0.2, 0.0],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )

    p.addUserDebugText(
        "A = POSICION INICIAL",
        [0.2, 0.2, -0.1],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )

    p.addUserDebugText(
        "X = SALIR",
        [0.2, 0.2, -0.2],
        textColorRGB=[1, 1, 1],
        textSize=1.0
    )


    # --------------------------------------------------------
    # COMANDO ACTUAL
    # --------------------------------------------------------

    comando = "0"


    # --------------------------------------------------------
    # BUCLE PRINCIPAL
    # --------------------------------------------------------

    ejecutando = True

    while ejecutando:

        # ----------------------------------------------------
        # LEER ESP32
        # ----------------------------------------------------

        if esp32.in_waiting:

            datos = esp32.read(
                esp32.in_waiting
            )

            for byte in datos:

                tecla = chr(byte).upper()

                print("Tecla:", tecla)

                # --------------------------------------------
                # DETENER
                # --------------------------------------------

                if tecla == "0":

                    comando = "0"


                # --------------------------------------------
                # ARRIBA
                # --------------------------------------------

                elif tecla == "1":

                    comando = "1"


                # --------------------------------------------
                # ABAJO
                # --------------------------------------------

                elif tecla == "2":

                    comando = "2"


                # --------------------------------------------
                # IZQUIERDA
                # --------------------------------------------

                elif tecla == "4":

                    comando = "4"


                # --------------------------------------------
                # DERECHA
                # --------------------------------------------

                elif tecla == "6":

                    comando = "6"


                # --------------------------------------------
                # ADELANTE
                # --------------------------------------------

                elif tecla == "8":

                    comando = "8"


                # --------------------------------------------
                # ATRÁS
                # --------------------------------------------

                elif tecla == "5":

                    comando = "5"


                # --------------------------------------------
                # POSICIÓN INICIAL
                # --------------------------------------------

                elif tecla == "A":

                    comando = "A"


                # --------------------------------------------
                # SALIR
                # --------------------------------------------

                elif tecla == "X":

                    ejecutando = False


        # ----------------------------------------------------
        # MOVIMIENTO CONTINUO
        # ----------------------------------------------------

        if comando == "1":

            posicion_objetivo[2] += VELOCIDAD

        elif comando == "2":

            posicion_objetivo[2] -= VELOCIDAD

        elif comando == "4":

            posicion_objetivo[0] -= VELOCIDAD

        elif comando == "6":

            posicion_objetivo[0] += VELOCIDAD

        elif comando == "8":

            posicion_objetivo[1] += VELOCIDAD

        elif comando == "5":

            posicion_objetivo[1] -= VELOCIDAD

        elif comando == "A":

            posicion_objetivo = posicion_inicial.copy()

            comando = "0"


        # ----------------------------------------------------
        # LIMITES DE SEGURIDAD
        # ----------------------------------------------------

        posicion_objetivo[0] = max(
            -0.2,
            min(0.9, posicion_objetivo[0])
        )

        posicion_objetivo[1] = max(
            -0.5,
            min(0.8, posicion_objetivo[1])
        )

        posicion_objetivo[2] = max(
            -0.5,
            min(0.5, posicion_objetivo[2])
        )


        # ----------------------------------------------------
        # SUAVIZAR EL MOVIMIENTO
        # ----------------------------------------------------

        posicion_actual = mover_suave(
            posicion_actual,
            posicion_objetivo
        )


        # ----------------------------------------------------
        # CINEMÁTICA INVERSA
        # ----------------------------------------------------

        jointPoses = calcular_IK(
            baxterId,
            posicion_actual,
            lowerLimits,
            upperLimits,
            jointRanges,
            restPoses
        )


        # ----------------------------------------------------
        # CONTROL DE MOTORES
        # ----------------------------------------------------

        mover_brazo(
            baxterId,
            jointPoses
        )


        # ----------------------------------------------------
        # SIMULACIÓN
        # ----------------------------------------------------

        p.stepSimulation()

        time.sleep(1 / 240)


    # --------------------------------------------------------
    # CERRAR
    # --------------------------------------------------------

    print("Cerrando simulación...")

    esp32.close()

    p.disconnect()

    print("Programa finalizado.")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    main()