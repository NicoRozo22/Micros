import pybullet as p
import pybullet_data
import time
import serial
import math

# ==========================================
# CONEXIÓN ESP32
# ==========================================

arduino = serial.Serial("COM3", 115200, timeout=0.05)
time.sleep(2)
arduino.reset_input_buffer()

print("ESP32 conectado por COM3")


# ==========================================
# PYBULLET
# ==========================================

physics_client = p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

robot_id = p.loadURDF(
    "brazo.urdf",
    [0, 0, 0.15],
    useFixedBase=True
)

print("Brazo cargado correctamente")


# ==========================================
# VARIABLES
# ==========================================

joint0_target = 0.0
joint1_target = 0.0
gripper_target = 0.0

dedo_izq_target = 0.025
dedo_der_target = 0.025

BASE_Z = 0.65
LONGITUD_BRAZO = 0.30


# ==========================================
# ACTUALIZAR BRAZO
# ==========================================

def actualizar_brazo():

    p.setJointMotorControl2(
        robot_id, 0,
        p.POSITION_CONTROL,
        targetPosition=joint0_target,
        force=100,
        maxVelocity=1.0
    )

    p.setJointMotorControl2(
        robot_id, 1,
        p.POSITION_CONTROL,
        targetPosition=joint1_target,
        force=80,
        maxVelocity=1.0
    )

    p.setJointMotorControl2(
        robot_id, 2,
        p.POSITION_CONTROL,
        targetPosition=gripper_target,
        force=40,
        maxVelocity=0.5
    )

    p.setJointMotorControl2(
        robot_id, 3,
        p.POSITION_CONTROL,
        targetPosition=dedo_izq_target,
        force=20,
        maxVelocity=0.2
    )

    p.setJointMotorControl2(
        robot_id, 4,
        p.POSITION_CONTROL,
        targetPosition=dedo_der_target,
        force=20,
        maxVelocity=0.2
    )


# ==========================================
# MOVER PUNTA
# ==========================================

def mover_punta(x, z):

    global joint1_target
    global gripper_target

    argumento = x / LONGITUD_BRAZO

    argumento = max(
        -0.95,
        min(0.95, argumento)
    )

    joint1_target = math.asin(argumento)

    altura_brazo = (
        BASE_Z +
        LONGITUD_BRAZO *
        math.cos(joint1_target)
    )

    gripper_target = z - altura_brazo

    gripper_target = max(
        0.0,
        min(0.15, gripper_target)
    )

    actualizar_brazo()


# ==========================================
# EJECUTAR TRAYECTORIA
# ==========================================

def ejecutar_trayectoria(puntos):

    for i in range(len(puntos) - 1):

        x1, z1 = puntos[i]
        x2, z2 = puntos[i + 1]

        pasos = 30

        for j in range(pasos + 1):

            t = j / pasos

            x = x1 + (x2 - x1) * t
            z = z1 + (z2 - z1) * t

            mover_punta(x, z)

            for k in range(3):

                p.stepSimulation()

                time.sleep(0.01)


# ==========================================
# CONFIGURACIÓN DE LOS NÚMEROS
# ==========================================

X = 0.0
Z = 0.90

ANCHO = 0.10
ALTO = 0.15

IZQ = X - ANCHO / 2
DER = X + ANCHO / 2

ARRIBA = Z + ALTO
MEDIO = Z + ALTO / 2
ABAJO = Z


# ==========================================
# NÚMERO 0
# ==========================================

def dibujar_0():

    print("Dibujando NUMERO 0")

    puntos = [
        (IZQ, MEDIO),
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (DER, ABAJO),
        (IZQ, ABAJO),
        (IZQ, MEDIO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 1
# ==========================================

def dibujar_1():

    print("Dibujando NUMERO 1")

    puntos = [
        (0.00, ABAJO),
        (0.00, ARRIBA),
        (-0.04, Z + ALTO - 0.04),
        (0.00, ARRIBA)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 2
# ==========================================

def dibujar_2():

    print("Dibujando NUMERO 2")

    puntos = [
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (DER, MEDIO),
        (IZQ, ABAJO),
        (DER, ABAJO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 3
# ==========================================

def dibujar_3():

    print("Dibujando NUMERO 3")

    puntos = [
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (IZQ, MEDIO),
        (DER, MEDIO),
        (IZQ, ABAJO),
        (DER, ABAJO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 4
# ==========================================

def dibujar_4():

    print("Dibujando NUMERO 4")

    puntos = [
        (DER, ABAJO),
        (DER, ARRIBA),
        (IZQ, MEDIO),
        (DER, MEDIO),
        (IZQ, MEDIO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 5
# ==========================================

def dibujar_5():

    print("Dibujando NUMERO 5")

    puntos = [
        (DER, ARRIBA),
        (IZQ, ARRIBA),
        (IZQ, MEDIO),
        (DER, MEDIO),
        (DER, ABAJO),
        (IZQ, ABAJO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 6
# ==========================================

def dibujar_6():

    print("Dibujando NUMERO 6")

    puntos = [
        (DER, ARRIBA),
        (IZQ, ARRIBA),
        (IZQ, ABAJO),
        (DER, ABAJO),
        (DER, MEDIO),
        (IZQ, MEDIO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 7
# ==========================================

def dibujar_7():

    print("Dibujando NUMERO 7")

    puntos = [
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (IZQ, ABAJO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 8
# ==========================================

def dibujar_8():

    print("Dibujando NUMERO 8")

    puntos = [
        (IZQ, MEDIO),
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (DER, MEDIO),
        (IZQ, MEDIO),
        (IZQ, ABAJO),
        (DER, ABAJO),
        (DER, MEDIO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# NÚMERO 9
# ==========================================

def dibujar_9():

    print("Dibujando NUMERO 9")

    puntos = [
        (IZQ, MEDIO),
        (IZQ, ARRIBA),
        (DER, ARRIBA),
        (DER, ABAJO),
        (IZQ, ABAJO),
        (IZQ, MEDIO)
    ]

    ejecutar_trayectoria(puntos)


# ==========================================
# POSICIÓN INICIAL
# ==========================================

def posicion_inicial():

    global joint0_target
    global joint1_target
    global gripper_target

    joint0_target = 0.0
    joint1_target = 0.0
    gripper_target = 0.0

    actualizar_brazo()

    print("Brazo en posicion inicial")


# ==========================================
# MENÚ
# ==========================================

print("")
print("==========================================")
print("       BRAZO ROBOTICO - DIBUJANDO")
print("==========================================")
print("0 -> DIBUJAR 0")
print("1 -> DIBUJAR 1")
print("2 -> DIBUJAR 2")
print("3 -> DIBUJAR 3")
print("4 -> DIBUJAR 4")
print("5 -> DIBUJAR 5")
print("6 -> DIBUJAR 6")
print("7 -> DIBUJAR 7")
print("8 -> DIBUJAR 8")
print("9 -> DIBUJAR 9")
print("D -> POSICION INICIAL")
print("==========================================")


posicion_inicial()


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

while True:

    if arduino.in_waiting > 0:

        tecla = arduino.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if len(tecla) == 1 and tecla in "0123456789D":

            print("Tecla:", tecla)

            if tecla == "0":
                dibujar_0()

            elif tecla == "1":
                dibujar_1()

            elif tecla == "2":
                dibujar_2()

            elif tecla == "3":
                dibujar_3()

            elif tecla == "4":
                dibujar_4()

            elif tecla == "5":
                dibujar_5()

            elif tecla == "6":
                dibujar_6()

            elif tecla == "7":
                dibujar_7()

            elif tecla == "8":
                dibujar_8()

            elif tecla == "9":
                dibujar_9()

            elif tecla == "D":
                posicion_inicial()

    p.stepSimulation()

    time.sleep(0.01)