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

END_EFFECTOR_ID = 48

PASO = 0.05

# Posición inicial de la mano
TARGET_INICIAL = np.array([0.20, 0.0, -0.10], dtype=float)

# Posición encima/cerca del objeto
TARGET_OBJETO = np.array([0.45, 0.0, -0.25], dtype=float)

# Posición levantada
TARGET_LEVANTAR = np.array([0.45, 0.0, -0.05], dtype=float)

# Posición final
TARGET_DESTINO = np.array([0.65, 0.25, -0.05], dtype=float)

# Estado del agarre
objeto_agarrado = False


# ============================================================
# CREAR MUNDO
# ============================================================

def setUpWorld():

    p.resetSimulation()

    p.setGravity(0, 0, -10)

    p.setAdditionalSearchPath(
        pybullet_data.getDataPath()
    )

    # Piso
    p.loadURDF(
        "plane.urdf",
        [0, 0, -1],
        useFixedBase=True
    )

    time.sleep(0.2)

    # Cargar Baxter
    baxterId = p.loadURDF(
        "baxter_common/baxter_description/urdf/toms_baxter.urdf",
        useFixedBase=True
    )

    p.resetBasePositionAndOrientation(
        baxterId,
        [0.5, -0.8, 0.0],
        [0., 0., -1., -1.]
    )

    for _ in range(100):
        p.stepSimulation()

    return baxterId


# ============================================================
# RANGOS DE ARTICULACIONES
# ============================================================

def getJointRanges(bodyId):

    lowerLimits = []
    upperLimits = []
    jointRanges = []
    restPoses = []

    for i in range(p.getNumJoints(bodyId)):

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
# MOVER BRAZO
# ============================================================

def mover_brazo(
    baxterId,
    targetPosition,
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses
):

    jointPoses = calcular_IK(
        baxterId,
        targetPosition,
        lowerLimits,
        upperLimits,
        jointRanges,
        restPoses
    )

    for i in range(p.getNumJoints(baxterId)):

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

    return jointPoses


# ============================================================
# CREAR OBJETO
# ============================================================

def crear_objeto():

    mitad = [0.06, 0.06, 0.06]

    visual = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=mitad,
        rgbaColor=[0.1, 0.4, 1.0, 1.0]
    )

    collision = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=mitad
    )

    objeto = p.createMultiBody(
        baseMass=0.15,
        baseCollisionShapeIndex=collision,
        baseVisualShapeIndex=visual,
        basePosition=[0.45, 0.0, -0.70]
    )

    return objeto


# ============================================================
# COLOCAR OBJETO EN LA MANO
# ============================================================

def objeto_en_mano(
    baxterId,
    objeto
):

    linkState = p.getLinkState(
        baxterId,
        END_EFFECTOR_ID
    )

    posicion_mano = np.array(
        linkState[4]
    )

    # Pequeño desplazamiento para que el objeto
    # quede debajo de la mano
    posicion_objeto = posicion_mano + np.array(
        [0.0, 0.0, -0.08]
    )

    p.resetBasePositionAndOrientation(
        objeto,
        posicion_objeto,
        [0, 0, 0, 1]
    )


# ============================================================
# TEXTO
# ============================================================

def texto_estado(texto):

    p.addUserDebugText(
        texto,
        [0.0, 0.0, 1.55],
        textColorRGB=[1, 1, 0],
        textSize=1.4,
        lifeTime=2
    )

    print(texto)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print("========================================")
print("   BAXTER CONTROLADO CON ESP32")
print("========================================")


# ------------------------------------------------------------
# CONECTAR ESP32
# ------------------------------------------------------------

try:

    esp32 = serial.Serial(
        PUERTO_ESP32,
        BAUDRATE,
        timeout=0.05
    )

    esp32.reset_input_buffer()

    print("ESP32 conectado en", PUERTO_ESP32)

except Exception as error:

    print("ERROR AL CONECTAR EL ESP32")
    print(error)

    print()
    print("Verifica:")
    print("- ESP32 conectado")
    print("- Puerto COM3")
    print("- Monitor Serial cerrado")

    raise SystemExit


# ------------------------------------------------------------
# ABRIR PYBULLET
# ------------------------------------------------------------

cliente = p.connect(p.GUI)

if cliente < 0:

    print("No se pudo abrir PyBullet.")

    esp32.close()

    raise SystemExit


# ------------------------------------------------------------
# CARGAR BAXTER
# ------------------------------------------------------------

baxterId = setUpWorld()


# ------------------------------------------------------------
# CONFIGURAR CÁMARA
# ------------------------------------------------------------

p.resetDebugVisualizerCamera(
    cameraDistance=2.2,
    cameraYaw=180,
    cameraPitch=-10,
    cameraTargetPosition=[0.5, -0.2, 0.0]
)


# ------------------------------------------------------------
# RANGOS
# ------------------------------------------------------------

(
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses
) = getJointRanges(baxterId)


# ------------------------------------------------------------
# CREAR OBJETO
# ------------------------------------------------------------

objeto = crear_objeto()

print("OBJETO CREADO.")
print("El objeto azul debe aparecer desde el inicio.")


# ------------------------------------------------------------
# POSICIÓN INICIAL
# ------------------------------------------------------------

targetPosition = TARGET_INICIAL.copy()

mover_brazo(
    baxterId,
    targetPosition,
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses
)


# ------------------------------------------------------------
# INFORMACIÓN EN PYBULLET
# ------------------------------------------------------------

p.addUserDebugText(
    "BAXTER + ESP32",
    [0.0, 0.0, 1.40],
    textColorRGB=[0, 1, 0],
    textSize=1.5
)

p.addUserDebugText(
    "1 ARRIBA | 2 ABAJO",
    [0.0, 0.0, 1.25],
    textColorRGB=[1, 1, 1],
    textSize=1.1
)

p.addUserDebugText(
    "4 IZQ | 6 DER | 8 ADELANTE | 5 ATRAS",
    [0.0, 0.0, 1.15],
    textColorRGB=[1, 1, 1],
    textSize=1.0
)

p.addUserDebugText(
    "B = PREPARAR",
    [0.0, 0.0, 1.05],
    textColorRGB=[1, 1, 1],
    textSize=1.1
)

p.addUserDebugText(
    "C = AGARRAR / SOLTAR",
    [0.0, 0.0, 0.95],
    textColorRGB=[1, 1, 1],
    textSize=1.1
)

p.addUserDebugText(
    "D = LEVANTAR Y MOVER",
    [0.0, 0.0, 0.85],
    textColorRGB=[1, 1, 1],
    textSize=1.1
)


# ------------------------------------------------------------
# CONTROLES
# ------------------------------------------------------------

print()
print("----------------------------------------")
print("CONTROLES")
print("----------------------------------------")
print("1 = Arriba")
print("2 = Abajo")
print("4 = Izquierda")
print("6 = Derecha")
print("8 = Adelante")
print("5 = Atrás")
print("A = Posición inicial")
print("B = Preparar para coger")
print("C = Agarrar / soltar")
print("D = Levantar y mover")
print("X = Salir")
print("----------------------------------------")


# ------------------------------------------------------------
# BUCLE
# ------------------------------------------------------------

ejecutando = True

try:

    while ejecutando:

        # ================================================
        # LEER ESP32
        # ================================================

        if esp32.in_waiting > 0:

            datos = esp32.read(
                esp32.in_waiting
            )

            for byte in datos:

                tecla = chr(byte).upper()

                print("Tecla recibida:", tecla)


                # ============================================
                # MOVIMIENTO MANUAL
                # ============================================

                if tecla == "1":

                    targetPosition[2] += PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                elif tecla == "2":

                    targetPosition[2] -= PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                elif tecla == "4":

                    targetPosition[1] += PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                elif tecla == "6":

                    targetPosition[1] -= PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                elif tecla == "8":

                    targetPosition[0] += PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                elif tecla == "5":

                    targetPosition[0] -= PASO

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )


                # ============================================
                # POSICIÓN INICIAL
                # ============================================

                elif tecla == "A":

                    targetPosition = TARGET_INICIAL.copy()

                    objeto_agarrado = False

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )

                    # Regresar objeto a su posición inicial
                    p.resetBasePositionAndOrientation(
                        objeto,
                        [0.45, 0.0, -0.70],
                        [0, 0, 0, 1]
                    )

                    texto_estado(
                        "POSICION INICIAL"
                    )


                # ============================================
                # B = PREPARAR
                # ============================================

                elif tecla == "B":

                    print("B: preparando para coger objeto...")

                    targetPosition = TARGET_OBJETO.copy()

                    mover_brazo(
                        baxterId,
                        targetPosition,
                        lowerLimits,
                        upperLimits,
                        jointRanges,
                        restPoses
                    )

                    texto_estado(
                        "BRAZO SOBRE EL OBJETO"
                    )


                # ============================================
                # C = AGARRAR / SOLTAR
                # ============================================

                elif tecla == "C":

                    if not objeto_agarrado:

                        objeto_agarrado = True

                        texto_estado(
                            "OBJETO AGARRADO"
                        )

                        print(
                            "El objeto ahora sigue la mano."
                        )

                    else:

                        objeto_agarrado = False

                        texto_estado(
                            "OBJETO SOLTADO"
                        )

                        print(
                            "Objeto liberado."
                        )


                # ============================================
                # D = LEVANTAR Y MOVER
                # ============================================

                elif tecla == "D":

                    if objeto_agarrado:

                        print(
                            "Levantando objeto..."
                        )

                        # Levantar
                        targetPosition = TARGET_LEVANTAR.copy()

                        mover_brazo(
                            baxterId,
                            targetPosition,
                            lowerLimits,
                            upperLimits,
                            jointRanges,
                            restPoses
                        )

                        # Esperar y mantener objeto en la mano
                        for _ in range(180):

                            p.stepSimulation()

                            objeto_en_mano(
                                baxterId,
                                objeto
                            )

                            time.sleep(
                                1 / 240
                            )


                        print(
                            "Moviendo objeto al destino..."
                        )

                        # Mover al destino
                        targetPosition = TARGET_DESTINO.copy()

                        mover_brazo(
                            baxterId,
                            targetPosition,
                            lowerLimits,
                            upperLimits,
                            jointRanges,
                            restPoses
                        )

                        for _ in range(240):

                            p.stepSimulation()

                            objeto_en_mano(
                                baxterId,
                                objeto
                            )

                            time.sleep(
                                1 / 240
                            )

                        texto_estado(
                            "OBJETO MOVIDO"
                        )

                    else:

                        print(
                            "Primero presiona B y después C."
                        )


                # ============================================
                # X = SALIR
                # ============================================

                elif tecla == "X":

                    ejecutando = False

                    break


        # ====================================================
        # SIMULACIÓN CONTINUA
        # ====================================================

        p.stepSimulation()


        # Si el objeto está agarrado,
        # mantenerlo junto a la mano
        if objeto_agarrado:

            objeto_en_mano(
                baxterId,
                objeto
            )


        time.sleep(
            1 / 240
        )


except KeyboardInterrupt:

    print("Programa detenido.")


finally:

    try:
        esp32.close()
    except:
        pass

    try:
        p.disconnect()
    except:
        pass

    print("Programa finalizado.")