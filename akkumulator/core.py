from influxdb import InfluxDBClient
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('config.json')

devices = config.devices
if config.environment == "production":
    config = config.production
else:
    config = config.develop

client = InfluxDBClient('herbert', 8086, 'root', 'root', 'tasmotaToInflux')

def getDatabases():
    rs = client.query("show databases")
    names = []
    for n in rs['databases']:
        name = n['name']
        if name != '_internal':
            names.append(name)
            #getSeries(name)
    return names

def getSeries(db, m):
    rs = client.query("SHOW SERIES ON " + db + " FROM  " + m)
    for m in rs.get_points():
        print(m.sp)

def getTags(db):
    rs = client.query("SHOW TAG KEYS ON " + db)
    for m in rs.get_points():
        print(m)

def getMeasurements(db):
    rs = client.query("SHOW MEASUREMENTS ON " + db)
    names = []
    for m in rs.get_points():
        name = m['name']
        names.append(name)
    return names


def ShowResultOf(str):
    resultset = client.query(str)
    print(resultset)
    print(resultset.raw)


def Core():
    print('[init] core started')
    print('[init] influxdb databases: ' + str(getDatabases()))
    print('[init] we look into: ' + str(config.databases))
    for c in config.databases:
        #getSeries(c)
        measurements = getMeasurements(c)
        getTags(c)
        for m in measurements:
            s = getSeries(c,m)
            #print(s)
#    ShowResultOf("show databases")
#    ShowResultOf(
#        'SELECT mean("Power") FROM "ew_steckdosen" WHERE  time > now() -1d AND time < now() GROUP BY time(1h) fill(none)')
