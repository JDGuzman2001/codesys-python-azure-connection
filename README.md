# MQTT to Azure IoT Hub Bridge

Este proyecto implementa un puente (bridge) entre un broker MQTT y Azure IoT Hub, específicamente diseñado para la adecuación de leche. El sistema captura datos de diversos sensores y actuadores, los procesa y los envía a Azure IoT Hub para su posterior análisis y almacenamiento.

## Características

- Conexión segura a broker MQTT mediante SSL/TLS
- Procesamiento de múltiples tópicos MQTT
- Envío de datos a Azure IoT Hub
- Almacenamiento local en CSV como respaldo
- Manejo de variables de entorno para configuración segura
- Procesamiento específico para valores numéricos

## Requisitos Previos

- Python 3.8 o superior
- Cuenta en HiveMQ Cloud (o broker MQTT compatible)
- Cuenta en Azure con IoT Hub configurado
- Pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/JDGuzman2001/codesys-python-azure-connection.git
cd codesys-python-azure-connection
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
   - Copiar `.env.example` a `.env`
   - Completar las variables en `.env` con tus credenciales

## Configuración

### Variables de Entorno
Crear un archivo `.env` con las siguientes variables:

```plaintext
# MQTT Configuration
MQTT_BROKER=your_broker_url
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password

# Azure IoT Hub Configuration
AZURE_IOT_CONNECTION_STRING=your_connection_string
```

## Tópicos MQTT Soportados

El sistema procesa los siguientes tópicos:
- hivemqcloud (START)
- hivemqcloud1 (B1)
- hivemqcloud2 (SENSOR_ENTRADA)
- hivemqcloud3 (LECHE_REQUERIDA)
- hivemqcloud4 (B2)
- hivemqcloud5 (B3)
- hivemqcloud6 (B4)
- hivemqcloud7 (C1)
- hivemqcloud8 (MEZCLADOR)
- hivemqcloud9 (TEMP_REQUERIDA_SALIDA)
- hivemqcloud10 (SENSOR_TEMPE_SAL)
- hivemqcloud11 (SENSOR_TEMPE_MEZ)
- hivemqcloud12 (TEMP_REQUERIDA_INT)
- hivemqcloud13 (V1)

## Uso

1. Asegúrate de tener todas las variables de entorno configuradas
2. Ejecuta el script:
```bash
python main.py
```

## Estructura de Datos

Los datos se almacenan en formato CSV y se envían a Azure IoT Hub con la siguiente estructura:

```json
{
    "topic": "nombre_del_topico",
    "name": "nombre_del_sensor",
    "value": valor_numerico,
    "timestamp": "fecha_y_hora"
}
```

## Manejo de Errores

El sistema incluye manejo de errores para:
- Fallos en la conexión MQTT
- Errores en la decodificación de mensajes JSON
- Problemas de conexión con Azure IoT Hub
- Validación de tipos de datos

