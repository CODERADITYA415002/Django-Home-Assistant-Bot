"""
mqtt_communication.py
Communication and Control Module for the Django Home Assistant AI Bot.

Handles bidirectional MQTT communication between the bot's software layer
and the companion mobile application, using the Mosquitto broker as
described in the project report.

Requires: paho-mqtt  (pip install paho-mqtt --break-system-packages)
"""

import json

import paho.mqtt.client as mqtt

import config


class DjangoMQTTClient:
    def __init__(self, on_command_callback=None):
        """
        on_command_callback: function(command_dict) called whenever a new
        command is received on the commands topic.
        """
        self.on_command_callback = on_command_callback
        self.client = mqtt.Client()
        self.client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def connect(self):
        self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Connected with result code {rc}")
        client.subscribe(config.MQTT_TOPIC_COMMANDS)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {"raw": msg.payload.decode(errors="ignore")}

        print(f"[MQTT] Message received on {msg.topic}: {payload}")

        if self.on_command_callback:
            self.on_command_callback(payload)

    def publish_alert(self, sensor_type, message):
        """Publish a hazard/alert notification to the alerts topic."""
        payload = json.dumps({"sensor_type": sensor_type, "message": message})
        self.client.publish(config.MQTT_TOPIC_ALERTS, payload)
        print(f"[MQTT] Alert published: {payload}")

    def publish_status(self, status_dict):
        """Publish a general status/telemetry update."""
        payload = json.dumps(status_dict)
        self.client.publish(config.MQTT_TOPIC_STATUS, payload)
        print(f"[MQTT] Status published: {payload}")


if __name__ == "__main__":
    def handle_command(cmd):
        print("Handling command from app:", cmd)

    bot_client = DjangoMQTTClient(on_command_callback=handle_command)
    bot_client.connect()

    # Example status publish
    bot_client.publish_status({"battery": "87%", "mode": "standby"})

    import time
    time.sleep(5)
    bot_client.disconnect()
