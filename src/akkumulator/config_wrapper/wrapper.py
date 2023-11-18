from __future__ import annotations

from dataclasses import dataclass

from akkumulator.config_wrapper.types import InfluxDB
from akkumulator.config_wrapper.types import MqttBroker


@dataclass
class ConfigWrapper:
    mqtt: MqttBroker
    influxdb: InfluxDB