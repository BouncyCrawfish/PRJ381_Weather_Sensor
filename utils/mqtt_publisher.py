"""
MQTT publisher - sends each reading as JSON to your cloud broker/topic.

This is deliberately generic (plain MQTT) so it works whether your cloud
teammate is using AWS IoT Core, a Firebase MQTT bridge, HiveMQ, or a
self-hosted Mosquitto broker - only config.py needs to change per broker.

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
    MQTT_USE_TLS,
    MQTT_USERNAME,
    MQTT_PASSWORD,
)


class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)

        if MQTT_USERNAME:
            self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

        if MQTT_USE_TLS:
            self.client.tls_set()

        self.client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        self.client.loop_start()  # handles reconnects/network in background

    def publish(self, reading: dict):
        """Publishes one reading dict as a JSON payload."""
        payload = json.dumps(reading)
        result = self.client.publish(MQTT_TOPIC, payload, qos=1)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    publisher = MQTTPublisher()
    ok = publisher.publish({"test": "hello from IWOS station"})
    print("Published:", ok)
    publisher.close()
