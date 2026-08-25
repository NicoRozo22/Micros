import speech_recognition as sr
import serial
import time

# Puerto serial del ESP32
ESP32_PORT = "COM3"
BAUDRATE = 115200

# Conectar con el ESP32
try:
    esp32 = serial.Serial(ESP32_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print("ESP32 conectado correctamente.")
except:
    esp32 = None
    print("No se pudo conectar con el ESP32.")
    print("Verifique el puerto COM.")

# Reconocimiento de voz
recognizer = sr.Recognizer()

print("--------------------------------")
print("CHATBOT DOMÓTICO CON ESP32")
print("--------------------------------")
print("Diga un comando:")
print("- Enciende el LED")
print("- Apaga el LED")
print("- Salir")

while True:

    with sr.Microphone() as source:

        print("\nEscuchando...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            comando = recognizer.recognize_google(
                audio,
                language="es-ES"
            ).lower()

            print("Comando detectado:", comando)

            # ENCENDER LED
            if "enciende" in comando or "encender" in comando:

                if esp32:
                    esp32.write(b"ENCENDER\n")

                print("LED ENCENDIDO")

            # APAGAR LED
            elif "apaga" in comando or "apagar" in comando:

                if esp32:
                    esp32.write(b"APAGAR\n")

                print("LED APAGADO")

            # SALIR
            elif "salir" in comando or "terminar" in comando:

                print("Cerrando chatbot...")
                break

            else:

                print("Comando no reconocido.")

        except sr.WaitTimeoutError:

            print("No se detectó ningún comando.")

        except sr.UnknownValueError:

            print("No se pudo entender el comando.")

        except sr.RequestError:

            print("Error en el servicio de reconocimiento de voz.")

# Cerrar comunicación
if esp32:
    esp32.close()

print("Programa terminado.")
