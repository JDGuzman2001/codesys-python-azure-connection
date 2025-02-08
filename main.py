import paho.mqtt.client as mqtt
import json
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import datetime
import csv
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del servidor MQTT
BROKER = os.getenv('MQTT_BROKER')
PORT = int(os.getenv('MQTT_PORT', 8883))
TOPICS = ["hivemqcloud"] + [f"hivemqcloud{i}" for i in range(1, 14)]  # Tópicos desde hivemqcloud1 hasta hivemqcloud13
USERNAME = os.getenv('MQTT_USERNAME')
PASSWORD = os.getenv('MQTT_PASSWORD')

# Define connection string de Azure IoT Hub
connectionString = os.getenv('AZURE_IOT_CONNECTION_STRING')

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
        message = json.loads(msg.payload.decode())

        if "values" in message and len(message["values"]) > 0:
            v_value = message["values"][0].get("v", None)
            if v_value is not None:
                # Verificar si el valor es numérico pero NO es booleano
                if isinstance(v_value, (int, float)) and not isinstance(v_value, bool):
                    print(f"Valor numérico 'v' recibido en el tópico {msg.topic}: {v_value}")

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

                    timestamp = str(datetime.datetime.now())
                    data = {
                        "topic": msg.topic,
                        "name": name,
                        "value": v_value,
                        "timestamp": timestamp
                    }

                    # Solo guardar en CSV si el valor es numérico y no booleano
                    csv_file = 'sensor_data.csv'
                    file_exists = os.path.isfile(csv_file)
                    
                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=['timestamp', 'topic', 'name', 'value'])
                        if not file_exists:
                            writer.writeheader()
                        writer.writerow(data)

                    # Enviar el JSON a Azure IoT Hub
                    asyncio.run(send_to_iot_hub(data=json.dumps(data)))
                else:
                    print(f"Valor no numérico o booleano ignorado en el tópico {msg.topic}: {v_value}")
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
