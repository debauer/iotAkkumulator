from __future__ import annotations

import time
import csv
import logging
from argparse import Namespace, ArgumentParser
from logging import getLogger

from akkumulator.database.wrapper import InfluxWrapper

_log = getLogger("default")
ch = logging.StreamHandler()
_log.addHandler(ch)

UPDATE_EVERY_SEC = 300


def parse() -> Namespace:
    parser = ArgumentParser(description="System to record the data on a trimodal crane")
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_const",
        const="dryrun",
        help="don't commit to influxdb",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const="verbose",
        help="verbose",
    )
    return parser.parse_args()


def core():
    args = parse()
    _log.setLevel(logging.INFO)
    if args.verbose:
        _log.setLevel(logging.DEBUG)

    db = InfluxWrapper()

    _log.info('core started')
    db_list = db.get_databases()
    _log.info('influxdb databases: ' + str(db.get_databases()))
    for db_name in db_list:
        _log.info(f"influxdb series of {db_name}: {db.get_series(database=db_name)}")
    for db_name in db_list:
        _log.info(f"influxdb tags of {db_name}: {db.get_tags(database=db_name)}")
    # for db_name in db_list:
    #    _log.info(f"influxdb fields of {db_name}: {db.get_fields(database=db_name)}")
    db_name = "tasmota"
    all_devices = db.get_devices(database=db_name)
    for dev in all_devices:
        _log.info(f"influxdb tasmota devices: {dev}")
    _log.info(db.get_yesterday(database=db_name))

    while 1:
        with open('/srv/csv/power_per_day.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', )
            writer.writerow(['date', 'nicedate', "value"])
            yesterday = db.get_yesterday(database=db_name)
            yesterday.reverse()
            for day in yesterday:
                writer.writerow([day[0], str(day[0].date()).replace("-", "."), day[1]])
        time.sleep(UPDATE_EVERY_SEC)


if __name__ == "__main__":
    core()
