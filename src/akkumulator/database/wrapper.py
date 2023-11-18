import time
from datetime import datetime, timedelta
from logging import getLogger

from influxdb import InfluxDBClient

from akkumulator.config import MQTT_BROKER, INFLUX_DB
from akkumulator.config_wrapper.wrapper import ConfigWrapper
from akkumulator.helper.time import influx_time_to_datetime

_log = getLogger("default")


class InfluxWrapper:

    def __init__(self) -> None:
        self.config = ConfigWrapper(MQTT_BROKER, INFLUX_DB)
        self.client = InfluxDBClient(
            self.config.influxdb.address,
            self.config.influxdb.port,
            self.config.influxdb.user,
            self.config.influxdb.password
        )

    def get_databases(self):
        rs = self.client.query("show databases")
        names = []
        for n in rs['databases']:
            name = n['name']
            if name != '_internal':
                names.append(name)
        return names

    def _get_devices(self, database: str, series: str):
        rs = self.client.query("SHOW SERIES ON " + database + " FROM  " + series)
        names = []
        for m in rs.get_points():
            # _log.info(f"database: {database}, series: {series}, key: {m['key']}", "getDevices")
            names.append(m['key'])
        return names

    def get_tags(self, database: str):
        rs = self.client.query("SHOW TAG KEYS ON " + database)
        names = []
        for m in rs.get_points():
            tag_name = m['tagKey']
            if tag_name not in names:
                names.append(tag_name)
        return names

    def get_series(self, database: str):
        rs = self.client.query("SHOW MEASUREMENTS ON " + database)
        names = []
        for m in rs.get_points():
            name = m['name']
            names.append(name)
        return names

    def get_fields(self, database: str):
        rs = self.client.query("SHOW FIELD KEYS ON " + database)
        names = []
        for m in rs.get_points():
            name = m['fieldKey']
            names.append(name)
        return names

    def get_devices(self, database: str):
        series = self.get_series(database)
        plugs = []
        for serie in series:
            devices = self._get_devices(database, serie)
            for dev in devices:
                if "device_name" in dev:
                    split = dev.split(',')
                    series = split[0]
                    device_name = ""
                    alias = ""
                    for s in split:
                        if "device_name=" in s:
                            device_name = s.split('device_name=')[1]
                        if "alias_name=" in s:
                            alias = s.split('alias_name=')[1]

                    plugs.append([series, device_name, alias])
        return plugs

    def get_yesterday(self, database: str):
        fields = self.get_fields(database)
        print(fields)
        if "Yesterday" in fields:
            query = "SELECT first(Yesterday), last(Today) FROM ew_strom WHERE time <= '" + str(
                datetime.today().date()) + "T23:59:00Z' GROUP BY time(1d)"
            print(query)
            resultset = self.client.query(query, database=database)
            ret = []
            for result in resultset:
                ret = [(datetime.fromisoformat(a["time"]) - timedelta(days=1), a["first"]) for a in result]
                today = (datetime.fromisoformat(result[-1]["time"]), result[-1]["last"])
            ret.append(today)
            return ret

    def steckdosenVerbrauch(self, series: str, device: str, month: int, year: int):
        interval = 10  # seconds
        devider = 3600 / interval  # seconds per hour / interval
        start = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.now().replace(microsecond=0, second=0, minute=0)
        _log.info(datetime.now(), "before_query")
        query = f'SELECT Power FROM {series} WHERE "name" = \'{device}\' and Power < 500 and time > \'{start}\' and time < \'{end}\''
        resultset = self.client.query(query, database=read_db)
        total = 0
        data = {}
        _log.info(datetime.now(), "after_query")
        for result in resultset:
            for values in result:
                # print(influx_time_to_datetime(values["time"]))
                dt = influx_time_to_datetime(values["time"]).replace(second=0, minute=0, microsecond=0)
                if dt not in data:
                    data[dt] = values["Power"] / devider
                else:
                    data[dt] += values["Power"] / devider
        _log.info(datetime.now(), "after_databuild")
        # print(data)
        for key in data:
            _log.info(str(key) + " ==> " + str(data[key]), "device")
        # _log.info(total/devider, device)
        # client.delete_series(write_db, series, {"name": device})
