import pybullet as p
import serial
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

PUERTO = "COM3"
BAUDRATE = 115200

JOINT1_MIN = -2.5
JOINT1_MAX = 2.5

JOINT2_MIN = -2.0
JOINT2_MAX = 2.0

JOINT_1 = 0
JOINT_2 = 1

JOINT_GRIPPER = 2
JOINT_DEDO_IZQ = 3
JOINT_DEDO_DER = 4

DEDO_ABIERTO = 0.05
DEDO_CERRADO = 0.0


# ============================================================
# FUNCIÓN PARA CONVERTIR LOS POTENCIÓMETROS
# ============================================================

def mapear(valor, entrada_min, entrada_max,
           salida_min, salida_max):

    return salida_min + (
        (valor - entrada_min)
        * (salida_max - salida_min)
        / (entrada_max - entrada_min)
    )


# ============================================================
# FUNCIONES DEL GRIPPER
# ============================================================

def abrir_gripper():

    print("GRIPPER -> ABRIENDO")

    p.setJointMotorControl2(
        robot_id,
        JOINT_DEDO_IZQ,
        p.POSITION_CONTROL,
        targetPosition=DEDO_ABIERTO,
        force=100
    )

    p.setJointMotorControl2(
        robot_id,
        JOINT_DEDO_DER,
        p.POSITION_CONTROL,
        targetPosition=DEDO_ABIERTO,
        force=100
    )


def cerrar_gripper():

    print("GRIPPER -> CERRANDO")

    p.setJointMotorControl2(
        robot_id,
        JOINT_DEDO_IZQ,
        p.POSITION_CONTROL,
        targetPosition=DEDO_CERRADO,
        force=100
    )

    p.setJointMotorControl2(
        robot_id,
        JOINT_DEDO_DER,
        p.POSITION_CONTROL,
        targetPosition=DEDO_CERRADO,
        force=100
    )


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

print()
print("==============================================")
print("       ACTIVIDAD 5 - BRAZO ROBÓTICO")
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

    print("ESP32 conectado correctamente.")

except Exception as error:

    print("ERROR AL CONECTAR EL ESP32:")
    print(error)

    input("Presiona ENTER para cerrar...")

    exit()


# ============================================================
# INICIAR PYBULLET
# ============================================================

print()
print("Iniciando simulación...")

physicsClient = p.connect(p.GUI)

if physicsClient < 0:

    print("ERROR: No se pudo iniciar PyBullet.")

    arduino.close()

    input("Presiona ENTER para cerrar...")

    exit()


p.setGravity(0, 0, -9.81)


# ============================================================
# CARGAR EL BRAZO
# ============================================================

print("Cargando brazo.urdf...")

robot_id = p.loadURDF(
    "brazo.urdf",
    [0, 0, 0.15],
    useFixedBase=True
)

print("Brazo cargado correctamente.")
print()


# ============================================================
# MOSTRAR ARTICULACIONES
# ============================================================

print("Articulaciones del brazo:")

for i in range(p.getNumJoints(robot_id)):

    info = p.getJointInfo(robot_id, i)

    nombre = info[1].decode("utf-8")

    print("Joint", i, ":", nombre)

print()


# ============================================================
# POSICIÓN INICIAL
# ============================================================

p.resetJointState(
    robot_id,
    JOINT_1,
    0
)

p.resetJointState(
    robot_id,
    JOINT_2,
    0
)

p.resetJointState(
    robot_id,
    JOINT_GRIPPER,
    0
)

p.resetJointState(
    robot_id,
    JOINT_DEDO_IZQ,
    DEDO_CERRADO
)

p.resetJointState(
    robot_id,
    JOINT_DEDO_DER,
    DEDO_CERRADO
)


# ============================================================
# INFORMACIÓN DE CONTROL
# ============================================================

print("==============================================")
print("             CONTROL EN TIEMPO REAL")
print("==============================================")
print()

print("POT1 -> JOINT 1")
print("POT2 -> JOINT 2")

print()

print("TECLA 1 -> ABRIR GRIPPER")
print("TECLA 2 -> CERRAR GRIPPER")

print()

print("==============================================")
print()


ultima_muestra = time.time()


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

try:

    while p.isConnected():

        # ----------------------------------------------------
        # LEER DATOS DEL ESP32
        # ----------------------------------------------------

        if arduino.in_waiting > 0:

            linea = arduino.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()


            # ------------------------------------------------
            # ABRIR GRIPPER
            # ------------------------------------------------

            if linea == "OPEN":

                abrir_gripper()


            # ------------------------------------------------
            # CERRAR GRIPPER
            # ------------------------------------------------

            elif linea == "CLOSE":

                cerrar_gripper()


            # ------------------------------------------------
            # LEER POTENCIÓMETROS
            # ------------------------------------------------

            elif "," in linea:

                datos = linea.split(",")

                if len(datos) == 2:

                    try:

                        valor1 = int(datos[0])
                        valor2 = int(datos[1])


                        # Limitar valores
                        valor1 = max(
                            0,
                            min(4095, valor1)
                        )

                        valor2 = max(
                            0,
                            min(4095, valor2)
                        )


                        # ------------------------------------
                        # CONVERTIR POT1 A ÁNGULO
                        # ------------------------------------

                        angulo1 = mapear(
                            valor1,
                            0,
                            4095,
                            JOINT1_MIN,
                            JOINT1_MAX
                        )


                        # ------------------------------------
                        # CONVERTIR POT2 A ÁNGULO
                        # ------------------------------------

                        angulo2 = mapear(
                            valor2,
                            0,
                            4095,
                            JOINT2_MIN,
                            JOINT2_MAX
                        )


                        # ------------------------------------
                        # MOVER JOINT 1
                        # ------------------------------------

                        p.setJointMotorControl2(
                            robot_id,
                            JOINT_1,
                            p.POSITION_CONTROL,
                            targetPosition=angulo1,
                            force=100
                        )


                        # ------------------------------------
                        # MOVER JOINT 2
                        # ------------------------------------

                        p.setJointMotorControl2(
                            robot_id,
                            JOINT_2,
                            p.POSITION_CONTROL,
                            targetPosition=angulo2,
                            force=100
                        )


                        # ------------------------------------
                        # MOSTRAR DATOS
                        # ------------------------------------

                        ahora = time.time()

                        if ahora - ultima_muestra >= 0.3:

                            print(
                                "POT1:",
                                valor1,
                                "| POT2:",
                                valor2,
                                "| J1:",
                                round(angulo1, 2),
                                "| J2:",
                                round(angulo2, 2)
                            )

                            ultima_muestra = ahora


                    except ValueError:

                        pass


        # ----------------------------------------------------
        # ACTUALIZAR SIMULACIÓN
        # ----------------------------------------------------

        p.stepSimulation()

        time.sleep(0.01)


# ============================================================
# FINALIZAR
# ============================================================

except KeyboardInterrupt:

    print()
    print("Programa detenido por el usuario.")


finally:

    print()
    print("Cerrando conexiones...")


    try:

        arduino.close()

    except:

        pass


    try:

        if p.isConnected():

            p.disconnect()

    except:

        pass


    print("Programa finalizado.")