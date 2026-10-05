import pybullet as p
import serial
import time
import os
import numpy as np


# ============================================================
# CONFIGURACIÓN
# ============================================================

PUERTO = "COM3"
BAUDRATE = 115200

POT_MIN = 0
POT_MAX = 4095


# ============================================================
# CONEXIÓN ESP32
# ============================================================

print("==============================================")
print("      BAXTER + ESP32 + CINEMATICA INVERSA")
print("==============================================")

print()
print("Conectando con ESP32...")

try:

    esp32 = serial.Serial(
        PUERTO,
        BAUDRATE,
        timeout=0.01
    )

    time.sleep(2)

    print("ESP32 conectada correctamente.")

except Exception as e:

    print()
    print("ERROR AL CONECTAR CON LA ESP32:")
    print(e)

    exit()


# ============================================================
# UBICACIÓN DEL PROYECTO
# ============================================================

CARPETA = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DATA = os.path.join(
    CARPETA,
    "data"
)


# ============================================================
# RUTA DEL BAXTER
# ============================================================

ruta_baxter = os.path.join(
    DATA,
    "baxter_common",
    "baxter_description",
    "urdf",
    "toms_baxter.urdf"
)


print()
print("Ruta del Baxter:")
print(ruta_baxter)


if not os.path.exists(ruta_baxter):

    print()
    print("ERROR:")
    print("No se encontró el URDF de Baxter.")

    esp32.close()

    exit()


# ============================================================
# INICIAR PYBULLET
# ============================================================

print()
print("Iniciando PyBullet...")

cliente = p.connect(
    p.GUI
)


if cliente < 0:

    print("ERROR: No se pudo iniciar PyBullet.")

    esp32.close()

    exit()


# ============================================================
# CONFIGURACIÓN VISUAL
# ============================================================

p.setAdditionalSearchPath(
    DATA
)

p.setGravity(
    0,
    0,
    -10
)


# ============================================================
# CARGAR PLANO
# ============================================================

try:

    p.loadURDF(
        "plane.urdf",
        [0, 0, -1],
        useFixedBase=True
    )

except Exception:

    pass


# ============================================================
# CARGAR BAXTER
# ============================================================

print()
print("Cargando Baxter...")

baxter = p.loadURDF(
    ruta_baxter,
    useFixedBase=True
)

print("Baxter cargado correctamente.")


# ============================================================
# POSICIÓN DEL BAXTER
# ============================================================

p.resetBasePositionAndOrientation(
    baxter,
    [
        0.5,
        -0.8,
        0.0
    ],
    [
        0.0,
        0.0,
        -1.0,
        -1.0
    ]
)


# ============================================================
# CÁMARA
# ============================================================

p.resetDebugVisualizerCamera(
    cameraDistance=2.0,
    cameraYaw=180,
    cameraPitch=-15,
    cameraTargetPosition=[
        0.52,
        0.2,
        0.3
    ]
)


# ============================================================
# NÚMERO DE JOINTS
# ============================================================

numero_joints = p.getNumJoints(
    baxter
)


print()
print("Número de joints:")
print(numero_joints)


# ============================================================
# MOSTRAR JOINTS
# ============================================================

print()
print("==============================================")
print(" JOINTS DE BAXTER")
print("==============================================")


for i in range(
    numero_joints
):

    info = p.getJointInfo(
        baxter,
        i
    )

    nombre_joint = info[1].decode(
        "utf-8"
    )

    nombre_link = info[12].decode(
        "utf-8"
    )

    print(
        i,
        "|",
        nombre_joint,
        "|",
        nombre_link
    )


# ============================================================
# EFECTOR FINAL
# ============================================================

endEffectorId = 48


print()
print("==============================================")
print(" EFECTOR FINAL")
print("==============================================")


print(
    "End Effector:",
    endEffectorId
)


# ============================================================
# OBTENER RANGOS DE JOINTS
# ============================================================

def getJointRanges(
    bodyId,
    includeFixed=False
):

    lowerLimits = []

    upperLimits = []

    jointRanges = []

    restPoses = []


    numJoints = p.getNumJoints(
        bodyId
    )


    for i in range(
        numJoints
    ):

        jointInfo = p.getJointInfo(
            bodyId,
            i
        )


        qIndex = jointInfo[3]


        if (
            includeFixed
            or
            qIndex > -1
        ):

            lowerLimits.append(
                -2
            )

            upperLimits.append(
                2
            )

            jointRanges.append(
                2
            )

            restPoses.append(

                p.getJointState(
                    bodyId,
                    i
                )[0]

            )


    return (
        lowerLimits,
        upperLimits,
        jointRanges,
        restPoses
    )


# ============================================================
# OBTENER RANGOS
# ============================================================

(
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses
) = getJointRanges(
    baxter,
    includeFixed=False
)


# ============================================================
# POSICIÓN INICIAL DEL EFECTOR
# ============================================================

estadoInicial = p.getLinkState(
    baxter,
    endEffectorId
)


posicionInicial = list(
    estadoInicial[4]
)


print()
print("==============================================")
print(" POSICIÓN INICIAL DEL EFECTOR")
print("==============================================")


print(
    "X =",
    posicionInicial[0]
)

print(
    "Y =",
    posicionInicial[1]
)

print(
    "Z =",
    posicionInicial[2]
)


# ============================================================
# POSICIÓN OBJETIVO
# ============================================================

objetivo = posicionInicial.copy()


# ============================================================
# RECORRIDO
# ============================================================

RECORRIDO_X = 0.70

RECORRIDO_Z = 0.50


# ============================================================
# VALORES INICIALES DE POTENCIÓMETROS
# ============================================================

pot1 = 2048

pot2 = 2048


# ============================================================
# CONVERTIR POTENCIÓMETRO
# ============================================================

def convertir_potenciometro(
    valor
):

    if valor < POT_MIN:

        valor = POT_MIN


    if valor > POT_MAX:

        valor = POT_MAX


    porcentaje = (
        valor - POT_MIN
    ) / (
        POT_MAX - POT_MIN
    )


    return porcentaje


# ============================================================
# CINEMÁTICA INVERSA
# ============================================================

def accurateIK(

    bodyId,
    endEffectorId,
    targetPosition,
    lowerLimits,
    upperLimits,
    jointRanges,
    restPoses,
    maxIter=20,
    threshold=0.001

):

    closeEnough = False

    iteration = 0


    while (
        not closeEnough
        and
        iteration < maxIter
    ):


        # ----------------------------------------------------
        # CALCULAR IK
        # ----------------------------------------------------

        jointPoses = p.calculateInverseKinematics(

            bodyId,

            endEffectorId,

            targetPosition,

            lowerLimits=lowerLimits,

            upperLimits=upperLimits,

            jointRanges=jointRanges,

            restPoses=restPoses

        )


        # ----------------------------------------------------
        # APLICAR ARTICULACIONES
        # ----------------------------------------------------

        numJoints = p.getNumJoints(
            bodyId
        )


        for i in range(
            numJoints
        ):

            jointInfo = p.getJointInfo(
                bodyId,
                i
            )


            qIndex = jointInfo[3]


            if qIndex > -1:

                indice = qIndex - 7


                if (
                    indice >= 0
                    and
                    indice < len(jointPoses)
                ):

                    p.setJointMotorControl2(

                        bodyIndex=bodyId,

                        jointIndex=i,

                        controlMode=p.POSITION_CONTROL,

                        targetPosition=jointPoses[
                            indice
                        ],

                        force=500,

                        maxVelocity=2.0

                    )


        # ----------------------------------------------------
        # SIMULAR
        # ----------------------------------------------------

        p.stepSimulation()


        # ----------------------------------------------------
        # POSICIÓN REAL
        # ----------------------------------------------------

        linkState = p.getLinkState(

            bodyId,

            endEffectorId

        )


        nuevaPosicion = linkState[4]


        diferencia = [

            targetPosition[0]
            -
            nuevaPosicion[0],

            targetPosition[1]
            -
            nuevaPosicion[1],

            targetPosition[2]
            -
            nuevaPosicion[2]

        ]


        distancia = np.sqrt(

            diferencia[0] ** 2
            +
            diferencia[1] ** 2
            +
            diferencia[2] ** 2

        )


        closeEnough = (
            distancia < threshold
        )


        iteration += 1


    return jointPoses


# ============================================================
# INFORMACIÓN DEL CONTROL
# ============================================================

print()
print("==============================================")
print("       CONTROL CON POTENCIÓMETROS")
print("==============================================")


print()
print("POTENCIÓMETRO 1 -> X")

print(
    "0    -> izquierda"
)

print(
    "2048 -> centro"
)

print(
    "4095 -> derecha"
)


print()
print("POTENCIÓMETRO 2 -> Z")

print(
    "0    -> abajo"
)

print(
    "2048 -> centro"
)

print(
    "4095 -> arriba"
)


print()
print("Y permanece fija.")


print()
print("==============================================")


# ============================================================
# CONTROL DE TERMINAL
# ============================================================

ultimo_pot1 = -1000

ultimo_pot2 = -1000


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

try:

    while True:


        # ====================================================
        # LEER ESP32
        # ====================================================

        while esp32.in_waiting > 0:

            linea = esp32.readline().decode(

                "utf-8",

                errors="ignore"

            ).strip()


            if not linea:

                continue


            if linea.startswith(
                "POT,"
            ):

                datos = linea.split(",")


                if len(datos) == 3:

                    try:

                        pot1 = int(
                            datos[1]
                        )

                        pot2 = int(
                            datos[2]
                        )


                    except ValueError:

                        pass


        # ====================================================
        # CONVERTIR POTENCIÓMETROS
        # ====================================================

        porcentajeX = convertir_potenciometro(
            pot1
        )


        porcentajeZ = convertir_potenciometro(
            pot2
        )


        # ====================================================
        # CALCULAR X
        # ====================================================

        objetivo[0] = (

            posicionInicial[0]

            +

            (
                porcentajeX
                -
                0.5
            )

            *

            RECORRIDO_X

        )


        # ====================================================
        # MANTENER Y
        # ====================================================

        objetivo[1] = (
            posicionInicial[1]
        )


        # ====================================================
        # CALCULAR Z
        # ====================================================

        objetivo[2] = (

            posicionInicial[2]

            +

            (
                porcentajeZ
                -
                0.5
            )

            *

            RECORRIDO_Z

        )


        # ====================================================
        # LIMITAR X
        # ====================================================

        objetivo[0] = max(

            posicionInicial[0] - 0.35,

            min(

                posicionInicial[0] + 0.35,

                objetivo[0]

            )

        )


        # ====================================================
        # LIMITAR Z
        # ====================================================

        objetivo[2] = max(

            posicionInicial[2] - 0.25,

            min(

                posicionInicial[2] + 0.25,

                objetivo[2]

            )

        )


        # ====================================================
        # CALCULAR IK
        # ====================================================

        accurateIK(

            baxter,

            endEffectorId,

            objetivo,

            lowerLimits,

            upperLimits,

            jointRanges,

            restPoses,

            maxIter=5,

            threshold=0.002

        )


        # ====================================================
        # MOSTRAR DATOS
        # ====================================================

        if (

            abs(
                pot1
                -
                ultimo_pot1
            ) > 100

            or

            abs(
                pot2
                -
                ultimo_pot2
            ) > 100

        ):

            print()
            print("----------------------------------------------")

            print(
                "POT 1:",
                pot1
            )

            print(
                "POT 2:",
                pot2
            )

            print()

            print(
                "OBJETIVO X:",
                round(
                    objetivo[0],
                    3
                )
            )

            print(
                "OBJETIVO Y:",
                round(
                    objetivo[1],
                    3
                )
            )

            print(
                "OBJETIVO Z:",
                round(
                    objetivo[2],
                    3
                )
            )

            print("----------------------------------------------")


            ultimo_pot1 = pot1

            ultimo_pot2 = pot2


        time.sleep(
            0.01
        )


# ============================================================
# FINALIZAR
# ============================================================

except KeyboardInterrupt:

    print()
    print("Programa detenido.")


finally:

    try:

        esp32.close()

    except:

        pass


    if p.isConnected():

        p.disconnect()


    print()
    print("Programa finalizado.")