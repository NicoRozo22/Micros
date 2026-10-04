import pybullet as p
import pybullet_data
import serial
import time
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

PUERTO = "COM3"
BAUDRATE = 115200


# ============================================================
# ESP32
# ============================================================

print("Conectando con ESP32...")

try:
    esp32 = serial.Serial(
        PUERTO,
        BAUDRATE,
        timeout=0.01
    )

    time.sleep(2)

    print("ESP32 conectado correctamente.")

except Exception as e:

    print("ERROR COM3:")
    print(e)

    exit()


# ============================================================
# PYBULLET
# ============================================================

print("Iniciando PyBullet...")

p.connect(p.GUI)

p.setGravity(
    0,
    0,
    -9.81
)

CARPETA = os.path.dirname(
    os.path.abspath(__file__)
)

DATA = os.path.join(
    CARPETA,
    "data"
)

p.setAdditionalSearchPath(
    DATA
)


# ============================================================
# BAXTER
# ============================================================

ruta_baxter = os.path.join(
    DATA,
    "baxter_common",
    "baxter_description",
    "urdf",
    "toms_baxter.urdf"
)

print("Cargando Baxter...")

baxter = p.loadURDF(
    ruta_baxter,
    useFixedBase=True
)

print("Baxter cargado.")


# ============================================================
# PLANO
# ============================================================

p.loadURDF(
    "plane.urdf",
    [0, 0, -1]
)


# ============================================================
# BUSCAR JOINT
# ============================================================

def buscar_joint(nombre):

    for i in range(
        p.getNumJoints(baxter)
    ):

        info = p.getJointInfo(
            baxter,
            i
        )

        nombre_actual = info[1].decode(
            "utf-8"
        )

        if nombre_actual == nombre:

            return i

    return None


# ============================================================
# BRAZOS
# ============================================================

left_arm = buscar_joint(
    "left_s0"
)

right_arm = buscar_joint(
    "right_s0"
)

print(
    "Brazo izquierdo:",
    left_arm
)

print(
    "Brazo derecho:",
    right_arm
)


# ============================================================
# MOSTRAR JOINTS DE LAS PINZAS
# ============================================================

print()
print("PINZAS DE BAXTER:")

for i in range(
    p.getNumJoints(baxter)
):

    info = p.getJointInfo(
        baxter,
        i
    )

    nombre = info[1].decode(
        "utf-8"
    )

    if "gripper" in nombre.lower():

        print(
            i,
            nombre
        )


# ============================================================
# BUSCAR PINZAS
# ============================================================

left_finger = buscar_joint(
    "left_gripper_l_finger_joint"
)

right_finger = buscar_joint(
    "right_gripper_l_finger_joint"
)


# ============================================================
# FUNCIÓN DE MOVIMIENTO
# ============================================================

def mover_brazo(
    joint,
    posicion
):

    if joint is None:
        return

    p.setJointMotorControl2(

        bodyIndex=baxter,

        jointIndex=joint,

        controlMode=p.POSITION_CONTROL,

        targetPosition=posicion,

        force=1000,

        maxVelocity=10

    )


# ============================================================
# PINZAS
# ============================================================

def abrir_pinzas():

    if left_finger is not None:

        p.setJointMotorControl2(
            baxter,
            left_finger,
            p.POSITION_CONTROL,
            targetPosition=0.04,
            force=300,
            maxVelocity=5
        )

    if right_finger is not None:

        p.setJointMotorControl2(
            baxter,
            right_finger,
            p.POSITION_CONTROL,
            targetPosition=0.04,
            force=300,
            maxVelocity=5
        )

    print("PINZAS ABIERTAS")


def cerrar_pinzas():

    if left_finger is not None:

        p.setJointMotorControl2(
            baxter,
            left_finger,
            p.POSITION_CONTROL,
            targetPosition=0.0,
            force=300,
            maxVelocity=5
        )

    if right_finger is not None:

        p.setJointMotorControl2(
            baxter,
            right_finger,
            p.POSITION_CONTROL,
            targetPosition=0.0,
            force=300,
            maxVelocity=5
        )

    print("PINZAS CERRADAS")


# ============================================================
# OBJETO
# ============================================================

print("Creando objeto...")


colision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[
        0.07,
        0.07,
        0.07
    ]
)


visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[
        0.07,
        0.07,
        0.07
    ],
    rgbaColor=[
        0,
        1,
        0,
        1
    ]
)


objeto = p.createMultiBody(

    baseMass=0.5,

    baseCollisionShapeIndex=colision,

    baseVisualShapeIndex=visual,

    basePosition=[
        0.65,
        -0.35,
        0.10
    ]
)


print("Cubo creado.")


# ============================================================
# CONSTRAINT DEL OBJETO
# ============================================================

constraint_objeto = None


# ============================================================
# BUSCAR LINK DE LA MANO DERECHA
# ============================================================

def buscar_mano_derecha():

    mejor = None

    for i in range(
        p.getNumJoints(baxter)
    ):

        info = p.getJointInfo(
            baxter,
            i
        )

        nombre = info[12].decode(
            "utf-8"
        )

        if (
            "right" in nombre.lower()
            and
            "gripper" in nombre.lower()
        ):

            mejor = i

    return mejor


mano_derecha = buscar_mano_derecha()

print(
    "Mano derecha:",
    mano_derecha
)


# ============================================================
# AGARRAR OBJETO
# ============================================================

def agarrar_objeto():

    global constraint_objeto

    if constraint_objeto is not None:

        print("El objeto ya está agarrado.")

        return


    if mano_derecha is None:

        print("No se encontró la mano derecha.")

        return


    # Posición actual de la mano

    estado = p.getLinkState(
        baxter,
        mano_derecha
    )

    posicion_mano = estado[4]


    # Posición del objeto

    posicion_objeto = (
        p.getBasePositionAndOrientation(
            objeto
        )[0]
    )


    print(
        "Mano:",
        posicion_mano
    )

    print(
        "Objeto:",
        posicion_objeto
    )


    # --------------------------------------------------------
    # UNIR EL OBJETO A LA MANO
    # --------------------------------------------------------

    constraint_objeto = p.createConstraint(

        parentBodyUniqueId=baxter,

        parentLinkIndex=mano_derecha,

        childBodyUniqueId=objeto,

        childLinkIndex=-1,

        jointType=p.JOINT_FIXED,

        jointAxis=[
            0,
            0,
            0
        ],

        parentFramePosition=[
            0,
            0,
            0
        ],

        childFramePosition=[
            0,
            0,
            0
        ]
    )


    print()
    print("==============================")
    print("OBJETO AGARRADO")
    print("==============================")


# ============================================================
# SOLTAR OBJETO
# ============================================================

def soltar_objeto():

    global constraint_objeto

    if constraint_objeto is not None:

        p.removeConstraint(
            constraint_objeto
        )

        constraint_objeto = None

        print("OBJETO SOLTADO")


# ============================================================
# MENSAJE
# ============================================================

print()
print(
    "========================================"
)

print(
    " CONTROL DE BAXTER CON ESP32"
)

print(
    "========================================"
)

print(
    "GPIO34 -> BRAZO IZQUIERDO"
)

print(
    "GPIO35 -> BRAZO DERECHO"
)

print(
    "TECLA 1 -> ABRIR"
)

print(
    "TECLA 2 -> CERRAR + AGARRAR"
)

print(
    "========================================"
)


# ============================================================
# BUCLE
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


            # =================================================
            # POTENCIÓMETROS
            # =================================================

            if linea.startswith(
                "POT,"
            ):

                datos = linea.split(",")


                if len(datos) == 3:

                    try:

                        pot_34 = int(
                            datos[1]
                        )

                        pot_35 = int(
                            datos[2]
                        )


                        # -------------------------------------
                        # MISMA CONVERSIÓN PARA LOS DOS
                        # -------------------------------------

                        angulo_34 = (

                            -1.5
                            +
                            (
                                pot_34
                                /
                                4095.0
                            )
                            * 3.0

                        )


                        angulo_35 = (

                            -1.5
                            +
                            (
                                pot_35
                                /
                                4095.0
                            )
                            * 3.0

                        )


                        # -------------------------------------
                        # MOVER LOS DOS
                        # -------------------------------------

                        mover_brazo(
                            left_arm,
                            angulo_34
                        )

                        mover_brazo(
                            right_arm,
                            angulo_35
                        )


                    except ValueError:

                        pass


            # =================================================
            # TECLA 1
            # =================================================

            elif linea == "OPEN":

                abrir_pinzas()


            # =================================================
            # TECLA 2
            # =================================================

            elif linea == "CLOSE":

                cerrar_pinzas()

                # Esperar un poco para que cierre

                time.sleep(0.4)

                # Agarrar objeto

                agarrar_objeto()


        # ====================================================
        # SIMULACIÓN
        # ====================================================

        p.stepSimulation()

        time.sleep(
            0.005
        )


except KeyboardInterrupt:

    print(
        "Programa detenido."
    )


finally:

    try:

        esp32.close()

    except:

        pass


    if p.isConnected():

        p.disconnect()

    print(
        "Programa finalizado."
    )