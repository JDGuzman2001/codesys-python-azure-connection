# Python Code README: HiveMQ to Azure IoT Hub via CODESYS and KEPServer

This README explains the functionality of the Python script, which connects CODESYS to HiveMQ via KEPServer, processes the received MQTT messages, and forwards the relevant data to Microsoft Azure IoT Hub.

---

## **Overview**

This Python script demonstrates a complete integration pipeline:
1. **Receive data** from CODESYS via HiveMQ MQTT broker.
2. **Process incoming messages**, extract key data, and map topics to meaningful identifiers.
3. **Send processed data** to Microsoft Azure IoT Hub for further analysis or storage.

---

## **Prerequisites**

1. **HiveMQ Cloud Account**:
   - HiveMQ Broker URL, Port, Username, and Password.
   - MQTT topics used for data communication.
2. **Azure IoT Hub**:
   - Connection string for your Azure IoT device.
3. **Python Libraries**:
   - `paho-mqtt`: For handling MQTT communication.
   - `azure-iot-device`: For Azure IoT Hub integration.
   - `asyncio`: For asynchronous operations.
   - `json`: For encoding and decoding message payloads.
4. **CODESYS and KEPServerEX**:
   - Configured to send data to the specified HiveMQ broker topics.

---

## **Setup**

### 1. Install Required Python Libraries
Run the following command to install the necessary libraries:
```bash
pip install paho-mqtt azure-iot-device
```

### 2. Update Configuration
Edit the script to include your credentials and connection details:
- **HiveMQ Broker Settings**:
  ```python
  BROKER = "your-hivemq-broker-url"
  PORT = 8883
  USERNAME = "your-username"
  PASSWORD = "your-password"
  ```
- **Azure IoT Hub Connection String**:
  ```python
  connectionString = "your-azure-iot-hub-connection-string"
  ```

### 3. MQTT Topics
Ensure the topics match the ones configured in KEPServerEX:
```python
TOPICS = ["hivemqcloud"] + [f"hivemqcloud{i}" for i in range(1, 14)]
```

---

## **How It Works**

### 1. MQTT Connection
- The script connects to the HiveMQ broker using SSL/TLS for secure communication.
- On successful connection, it subscribes to predefined topics.

### 2. Message Handling
- The `on_message` function processes incoming MQTT messages:
  - Decodes the JSON payload.
  - Extracts the `v` value (key variable) from the message.
  - Maps the topic to a meaningful name (e.g., START, SENSOR_ENTRADA).

### 3. Azure IoT Hub Integration
- Extracted data is forwarded to Azure IoT Hub using the `send_to_iot_hub` function:
  - Includes the topic name, mapped identifier, value, and a timestamp.
  - Azure IoT SDK handles secure transmission.

### 4. Error Handling
- The script gracefully handles:
  - MQTT connection issues.
  - Message decoding errors.
  - Azure IoT Hub communication failures.

---

## **Execution**

Run the script using:
```bash
python your_script_name.py
```

---

## **Example Workflow**

1. **KEPServerEX publishes data** from CODESYS to HiveMQ under topic `hivemqcloud`.
2. **HiveMQ forwards the message** to this script.
3. The script processes the message:
   - Example payload:
     ```json
     {
         "values": [
             { "v": 123 }
         ]
     }
     ```
   - Mapped output:
     ```json
     {
         "topic": "hivemqcloud",
         "name": "START",
         "value": 123,
         "timestamp": "2024-11-30T12:34:56"
     }
     ```
4. **Azure IoT Hub receives the data** for further processing or visualization.

---

## **Potential Improvements**

- **Environment Variables**:
  Store sensitive data (credentials, connection strings) in environment variables.
- **Dynamic Topic Mapping**:
  Load topic mappings from a configuration file for better flexibility.
- **Batch Processing**:
  Optimize by batching MQTT messages for fewer Azure IoT Hub calls.

---

## **Support**

For any questions or issues, refer to:
- [HiveMQ Documentation](https://www.hivemq.com/docs/)
- [Azure IoT Hub Documentation](https://learn.microsoft.com/en-us/azure/iot-hub/)

--- 

## **Disclaimer**

Ensure proper security practices when handling sensitive credentials and data. Avoid hardcoding passwords and connection strings directly in the script.
