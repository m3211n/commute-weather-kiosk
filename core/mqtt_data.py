"""Thread-safe MQTT snapshot cache for framebuffer updaters."""

import json
import os
from threading import Lock
from typing import Any, Dict

import paho.mqtt.client as mqtt


class MqttData:
    def __init__(self) -> None:
        self.prefix = os.environ.get("MQTT_TOPIC_PREFIX", "commute/dashboard").rstrip("/")
        self.values: Dict[str, Any] = {}
        self._lock = Lock()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self) -> None:
        self.client.connect_async(os.environ.get("MQTT_HOST", "localhost"), int(os.environ.get("MQTT_PORT", "1883")), 60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        if not reason_code.is_failure:
            client.subscribe(f"{self.prefix}/#", qos=1)
            client.subscribe("weather/outdoor/#", qos=1)

    def _on_message(self, client, userdata, message) -> None:
        try:
            value = json.loads(message.payload)
        except json.JSONDecodeError:
            value = message.payload.decode("utf-8", errors="replace")
        with self._lock:
            self.values[message.topic] = value

    def get(self, topic: str, default: Any) -> Any:
        with self._lock:
            return self.values.get(topic, default)

    def snapshot(self, topic: str, default: Any) -> Any:
        value = self.get(f"{self.prefix}/{topic}", None)
        return value.get("data", default) if isinstance(value, dict) else default

    def updated_at(self, topic: str) -> str:
        value = self.get(f"{self.prefix}/{topic}", {})
        return value.get("updated_at", "") if isinstance(value, dict) else ""


data = MqttData()
