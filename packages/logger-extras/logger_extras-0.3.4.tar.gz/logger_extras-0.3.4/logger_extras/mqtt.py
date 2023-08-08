from __future__ import annotations

import json
import logging
from typing import Any

import paho.mqtt.client as mqtt


class MQTTHandler(logging.Handler):
    def __init__(
        self,
        host: str,
        topic: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = '',
        client_id: str = '',
        userdata: Any = None,
        protocol: int = mqtt.MQTTv311,
        qos: int = 0,
        transport: str = 'tcp',
        use_tls: bool | str = False,
        username: str = '',
        password: str = '',
        append_logger_name: bool = False,
        connected_topic: str = '',
    ):
        super().__init__()

        self._topic = topic
        self._qos = qos
        self._append_logger_name = append_logger_name
        self._connected_topic = connected_topic

        self.mqtt = mqtt.Client(
            client_id=client_id,
            userdata=userdata,
            protocol=protocol,
            transport=transport)

        if use_tls:
            self.mqtt.tls_set()
            if use_tls == 'insecure':
                self.mqtt.tls_insecure_set(True)

        if username:
            self.mqtt.username_pw_set(username, password)

        self.mqtt.on_connect = self._on_connect
        if self._connected_topic:
            # This must be set before connecting
            self.mqtt.will_set(
                self._connected_topic, '{"state": "disconnected"}', qos=1, retain=True)

        try:
            self.mqtt.connect(
                host=host,
                port=port,
                keepalive=keepalive,
                bind_address=bind_address)
        except (TimeoutError, ValueError, ConnectionRefusedError):
            print(f"Failed to connect to MQTT broker at {host}:{port}")
            return
        self.mqtt.loop_start()

    def _on_connect(
        self, client: mqtt.Client, userdata: Any, flags: dict[str, int], rc: int,
        properties: mqtt.Properties | None = None,
    ) -> None:
        if self._connected_topic:
            client.publish(
                self._connected_topic, '{"state": "connected"}', qos=1, retain=True)

    def __del__(self) -> None:
        if self._connected_topic:
            res = self.mqtt.publish(
                self._connected_topic, '{"state": "disconnected"}', qos=1, retain=True)
            try:
                res.wait_for_publish(1)
            except (ValueError, RuntimeError):
                pass
        self.mqtt.disconnect()
        self.mqtt.loop_stop()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if (
                self.mqtt._logger  # type: ignore[attr-defined]
                and record.name == self.mqtt._logger.name  # type: ignore[attr-defined]
            ):
                # Avoid sending log messages of the MQTT client itself
                return
            if self._append_logger_name:
                topic = f"{self._topic}/{record.name.replace('.', '/')}"
            else:
                topic = self._topic

            if self.mqtt.is_connected() is False:
                self.mqtt.reconnect()

            msg = self.format(record)

            _ = self.mqtt.publish(
                topic=topic,
                payload=json.dumps({
                    "timestamp": record.created,
                    "message": msg,
                    "raw_message": record.message,
                    "level": record.levelname,
                    "name": record.name,
                }),
                qos=self._qos)
            self.flush()
        except Exception:
            self.handleError(record)
