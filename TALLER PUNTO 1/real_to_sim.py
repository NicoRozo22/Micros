import time
import serial
import numpy as np
import pybullet as p

from gym_pybullet_drones.utils.enums import DroneModel, Physics
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.utils import sync


# ============================================================
# CONFIGURACIÓN
# ============================================================

PUERTO_ESP32 = "COM3"
BAUDRATE = 115200

SIMULATION_FREQ_HZ = 240
CONTROL_FREQ_HZ = 48

DRONE = DroneModel("cf2x")

NUM_DRONES = 3


# ============================================================
# LUGARES A, B Y C
# ============================================================

PUNTO_A = np.array([0.0, 0.0, 0.6])
PUNTO_B = np.array([1.2, 0.0, 0.6])
PUNTO_C = np.array([1.2, 1.2, 0.6])


# ============================================================
# FORMACIÓN DE LOS 3 DRONES
# ============================================================

# Los drones estarán separados para evitar que choquen.
#
#       DRON 1
#          |
#       DRON 2
#          |
#       DRON 3

FORMACION = np.array([
    [-0.35, 0.0, 0.0],
    [ 0.00, 0.0, 0.0],
    [ 0.35, 0.0, 0.0]
])


# ============================================================
# POSICIONES INICIALES
# ============================================================

INIT_XYZS = np.array([
    PUNTO_A + FORMACION[0],
    PUNTO_A + FORMACION[1],
    PUNTO_A + FORMACION[2]
])

INIT_RPYS = np.array([
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]
])


# ============================================================
# MENSAJE INICIAL
# ============================================================

print()
print("==========================================")
print("       REAL-TO-SIM - 3 DRONES")
print("==========================================")
print()
print("ESP32:")
print("1 -> LOS 3 DRONES VAN AL LUGAR A")
print("2 -> LOS 3 DRONES VAN AL LUGAR B")
print("3 -> LOS 3 DRONES VAN AL LUGAR C")
print("D -> LOS 3 DRONES REGRESAN A A")
print("X -> SALIR")
print()


# ============================================================
# CONEXIÓN ESP32
# ============================================================

try:

    esp32 = serial.Serial(
        PUERTO_ESP32,
        BAUDRATE,
        timeout=0.01
    )

    time.sleep(2)

    print("ESP32 conectada correctamente.")
    print("Puerto:", PUERTO_ESP32)

except Exception as e:

    print("ERROR AL CONECTAR LA ESP32")
    print(e)
    print()
    print("Verifica:")
    print("- ESP32 conectada por USB")
    print("- Puerto COM3")
    print("- Monitor Serial cerrado")

    raise SystemExit


# ============================================================
# CREAR SIMULACIÓN
# ============================================================

env = CtrlAviary(

    drone_model=DRONE,

    num_drones=NUM_DRONES,

    initial_xyzs=INIT_XYZS,

    initial_rpys=INIT_RPYS,

    physics=Physics("pyb"),

    neighbourhood_radius=10,

    pyb_freq=SIMULATION_FREQ_HZ,

    ctrl_freq=CONTROL_FREQ_HZ,

    gui=True,

    record=False,

    obstacles=False,

    user_debug_gui=False
)


# ============================================================
# CLIENTE PYBULLET
# ============================================================

PYB_CLIENT = env.getPyBulletClient()


# ============================================================
# MARCADORES A, B Y C
# ============================================================

# Punto A
p.addUserDebugText(
    "LUGAR A",
    PUNTO_A + np.array([0, 0, 0.25]),
    textSize=2,
    lifeTime=0,
    physicsClientId=PYB_CLIENT
)

# Punto B
p.addUserDebugText(
    "LUGAR B",
    PUNTO_B + np.array([0, 0, 0.25]),
    textSize=2,
    lifeTime=0,
    physicsClientId=PYB_CLIENT
)

# Punto C
p.addUserDebugText(
    "LUGAR C",
    PUNTO_C + np.array([0, 0, 0.25]),
    textSize=2,
    lifeTime=0,
    physicsClientId=PYB_CLIENT
)


# Líneas verticales de referencia

for punto in [PUNTO_A, PUNTO_B, PUNTO_C]:

    p.addUserDebugLine(
        punto,
        punto + np.array([0, 0, 0.5]),
        lineWidth=4,
        lifeTime=0,
        physicsClientId=PYB_CLIENT
    )


# ============================================================
# CONTROLADORES PID
# ============================================================

ctrl = [
    DSLPIDControl(drone_model=DRONE)
    for _ in range(NUM_DRONES)
]


# ============================================================
# OBJETIVO INICIAL
# ============================================================

centro_objetivo = PUNTO_A.copy()


# Cada dron tiene su propio objetivo.
objetivos = np.array([
    centro_objetivo + FORMACION[0],
    centro_objetivo + FORMACION[1],
    centro_objetivo + FORMACION[2]
])


print()
print("Los 3 drones están en el LUGAR A.")
print("Esperando instrucciones de la ESP32...")
print()


# ============================================================
# ACCIÓN INICIAL
# ============================================================

action = np.zeros((NUM_DRONES, 4))

START = time.time()


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # LEER ESP32
        # ----------------------------------------------------

        if esp32.in_waiting > 0:

            datos = esp32.read(esp32.in_waiting)

            for byte in datos:

                tecla = chr(byte).upper()

                print()
                print("TECLA RECIBIDA:", tecla)


                # ============================================
                # LUGAR A
                # ============================================

                if tecla == "1":

                    centro_objetivo = PUNTO_A.copy()

                    objetivos = np.array([
                        centro_objetivo + FORMACION[0],
                        centro_objetivo + FORMACION[1],
                        centro_objetivo + FORMACION[2]
                    ])

                    print(">>> LOS 3 DRONES VAN AL LUGAR A")


                # ============================================
                # LUGAR B
                # ============================================

                elif tecla == "2":

                    centro_objetivo = PUNTO_B.copy()

                    objetivos = np.array([
                        centro_objetivo + FORMACION[0],
                        centro_objetivo + FORMACION[1],
                        centro_objetivo + FORMACION[2]
                    ])

                    print(">>> LOS 3 DRONES VAN AL LUGAR B")


                # ============================================
                # LUGAR C
                # ============================================

                elif tecla == "3":

                    centro_objetivo = PUNTO_C.copy()

                    objetivos = np.array([
                        centro_objetivo + FORMACION[0],
                        centro_objetivo + FORMACION[1],
                        centro_objetivo + FORMACION[2]
                    ])

                    print(">>> LOS 3 DRONES VAN AL LUGAR C")


                # ============================================
                # REGRESAR A
                # ============================================

                elif tecla == "D":

                    centro_objetivo = PUNTO_A.copy()

                    objetivos = np.array([
                        centro_objetivo + FORMACION[0],
                        centro_objetivo + FORMACION[1],
                        centro_objetivo + FORMACION[2]
                    ])

                    print(">>> LOS 3 DRONES REGRESAN AL LUGAR A")


                # ============================================
                # SALIR
                # ============================================

                elif tecla == "X":

                    print(">>> FINALIZANDO SIMULACIÓN")

                    raise KeyboardInterrupt


        # ----------------------------------------------------
        # AVANZAR SIMULACIÓN
        # ----------------------------------------------------

        obs, reward, terminated, truncated, info = env.step(action)


        # ----------------------------------------------------
        # CONTROL PID DE LOS 3 DRONES
        # ----------------------------------------------------

        for i in range(NUM_DRONES):

            action[i, :], _, _ = ctrl[i].computeControlFromState(

                control_timestep=env.CTRL_TIMESTEP,

                state=obs[i],

                target_pos=objetivos[i],

                target_rpy=INIT_RPYS[i]
            )


        # ----------------------------------------------------
        # ACTUALIZAR SIMULACIÓN
        # ----------------------------------------------------

        env.render()


        # ----------------------------------------------------
        # SINCRONIZAR
        # ----------------------------------------------------

        sync(
            int(
                (time.time() - START)
                * CONTROL_FREQ_HZ
            ),
            START,
            env.CTRL_TIMESTEP
        )


# ============================================================
# FINALIZACIÓN
# ============================================================

except KeyboardInterrupt:

    print()
    print("Simulación finalizada.")


finally:

    esp32.close()

    env.close()

    print("ESP32 desconectada.")
    print("Simulación cerrada.")