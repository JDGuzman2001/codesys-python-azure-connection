import paho.mqtt.client as mqtt
import json
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import datetime

# Configuración del servidor MQTT
BROKER = "7449d089e59e402a8ba42b99c0f9b87b.s1.eu.hivemq.cloud"
PORT = 8883
TOPICS = ["hivemqcloud"] + [f"hivemqcloud{i}" for i in range(1, 14)]  # Tópicos desde hivemqcloud1 hasta hivemqcloud13
USERNAME = "jdguzmanj"  # Cambia por tu usuario de HiveMQ
PASSWORD = "JD.GuzmanJ2001."  # Cambia por tu contraseña de HiveMQ

# Define connection string de Azure IoT Hub
connectionString = "HostName=automatica3-iot-hub.azure-devices.net;DeviceId=start-codesys;SharedAccessKey=b1YAuFHwJTRW+eu3P0IZjBVQJhwNAMClaAMf3VVc714="

# Función para enviar datos a Azure IoT Hub
async def send_to_iot_hub(data):
    try:
        # Crear una instancia del cliente IoT Hub
        device_client = IoTHubDeviceClient.create_from_connection_string(connectionString)

        # Conectar el cliente
        await device_client.connect()

        # Enviar el mensaje
        await device_client.send_message(data)
        print("Mensaje enviado a IoT Hub:", data)

        # Cerrar la conexión del cliente
        await device_client.shutdown()

    except Exception as e:
        print("Error al enviar mensaje:", str(e))

# Función que se ejecuta al recibir un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        # Decodificar el payload y convertirlo a un diccionario
        message = json.loads(msg.payload.decode())

        # Acceder al valor "v" dentro del mensaje
        if "values" in message and len(message["values"]) > 0:
            v_value = message["values"][0].get("v", None)  # Obtener el valor de "v"
            if v_value is not None:
                print(f"Valor 'v' recibido en el tópico {msg.topic}: {v_value}")

                if msg.topic == "hivemqcloud":
                    name = f"START"
                elif msg.topic == "hivemqcloud1":
                    name = f"B1"
                elif msg.topic == "hivemqcloud2":
                    name = f"SENSOR_ENTRADA"
                elif msg.topic == "hivemqcloud3":
                    name = f"LECHE_REQUERIDA"
                elif msg.topic == "hivemqcloud4":
                    name = f"B2"
                elif msg.topic == "hivemqcloud5":
                    name = f"B3"
                elif msg.topic == "hivemqcloud6":
                    name = f"B4"
                elif msg.topic == "hivemqcloud7":
                    name = f"C1"
                elif msg.topic == "hivemqcloud8":
                    name = f"MEZCLADOR"
                elif msg.topic == "hivemqcloud9":
                    name = f"TEMP_REQUERIDA_SALIDA"
                elif msg.topic == "hivemqcloud10":
                    name = f"SENSOR_TEMPE_SAL"
                elif msg.topic == "hivemqcloud11":
                    name = f"SENSOR_TEMPE_MEZ"
                elif msg.topic == "hivemqcloud12":
                    name = f"TEMP_REQUERIDA_INT"
                elif msg.topic == "hivemqcloud13":
                    name = f"V1"
                else:
                    name = f"UNKNOWN_TOPIC = {v_value}"

                # Construir el mensaje para enviar a Azure IoT Hub
                data = {
                    "topic": msg.topic,
                    "name": name,
                    "value": v_value,
                    "timestamp": str(datetime.datetime.now())  # Marca de tiempo actual
                }

                # Enviar el JSON a Azure IoT Hub
                asyncio.run(send_to_iot_hub(data=json.dumps(data)))

            else:
                print(f"No se encontró el valor 'v' en el mensaje del tópico {msg.topic}")
        else:
            print(f"No se encontraron valores en el mensaje del tópico {msg.topic}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el mensaje del tópico {msg.topic}: {msg.payload.decode()}")
    except Exception as e:
        print(f"Error procesando el mensaje del tópico {msg.topic}: {e}")

# Función que se ejecuta al conectar al servidor MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Suscrito al tópico: {topic}")
    else:
        print(f"Fallo al conectar, código de error: {rc}")

# Configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)  # Establecer credenciales

# Habilitar conexión SSL/TLS
client.tls_set()  # Configura automáticamente los certificados del sistema

client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
try:
    print(f"Conectando al broker {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()
except Exception as e:
    print(f"Error al conectar o procesar mensajes: {e}")
