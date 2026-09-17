"""
MQTT publisher - sends each reading as JSON to your cloud broker/topic.

MQTT publisher for the IWOS weather station (Pi side) - AWS IoT Core version.

Install:
    pip3 install paho-mqtt --break-system-packages
"""

import json

import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
    MQTT_CLIENT_ID,
    MQTT_CA_PATH,
    MQTT_CERT_PATH,
    MQTT_KEY_PATH,
)


class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False)

        self.client.tls_set(
            ca_certs=MQTT_CA_PATH,
            certfile=MQTT_CERT_PATH,
            keyfile=MQTT_KEY_PATH,
        )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self._connected = False

        self.client.connect_async(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = (rc == 0)
        print("MQTT connected to AWS IoT Core" if self._connected
              else f"MQTT connect failed, rc={rc}")

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        print(f"MQTT disconnected (rc={rc}); paho will retry automatically")

    def publish(self, reading: dict, qos: int = 1) -> bool:
        payload = json.dumps(reading)
        result = self.client.publish(MQTT_TOPIC, payload, qos=qos)
        result.wait_for_publish(timeout=5)
        return result.is_published()

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
