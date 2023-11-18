from __future__ import annotations

from akkumulator.config_wrapper.types import InfluxDB
from akkumulator.config_wrapper.types import MqttBroker


dummy_pw = "eva"
MQTT_BROKER = MqttBroker(
    address="herbert",
    port=1883,
    auth=False,
    user="adam",
    password=dummy_pw,
)

INFLUX_DB = InfluxDB(
    address="herbert",
    user="tasmota",
    auth=True,
    port=8086,
    password="asdf",  # noqa: S106
    database_name="tasmota",
    bulk_size=5,
)
