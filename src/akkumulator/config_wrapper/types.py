from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MqttBroker:
    address: str
    port: int
    auth: bool
    user: str
    password: str


@dataclass
class InfluxDB:
    address: str
    user: str
    password: str
    auth: bool = True
    database_name: str = "tasmota"
    port: int = 8086
    bulk_size: int = 5
