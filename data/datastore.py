from enum import Enum
import json

from .info import PiCamInfo
from .mysql import MysqlStore

def modeMap(mode):
    return f"({mode.index}, '{mode.format}', {mode.width}, {mode.height}, {mode.fps})"


class DataMode(Enum):
    Battery = 1
    Cameras = 2
    Modes = 3

    def deleteSQL(self):
        if self == DataMode.Battery:
            return 'DELETE FROM battery WHERE timestamp < TIMESTAMPADD(DAY, -7, CURRENT_TIMESTAMP)'
        elif self == DataMode.Cameras:
            return 'DELETE FROM picam.cameras WHERE idx>=0'
        elif self == DataMode.Modes:
            return 'DELETE FROM picam.modes WHERE camera>=0'
        else:
            raise Exception('No such operating mode')

    def insertSQL(self,data):
        if self == DataMode.Battery:
            return f"INSERT INTO picam.battery (voltage, current, percentage) values {data}"
        elif self == DataMode.Cameras:
            return f"INSERT INTO picam.cameras (idx,model) values {data}"
        elif self == DataMode.Modes:
            return f"INSERT INTO picam.modes (camera, format, width, height, fps) values {data}"
        else:
            raise Exception('No such operating mode')

    def readSQL(self):
        if self == DataMode.Battery:
            return 'select timestamp, percentage from picam.battery where timestamp = (SELECT max(timestamp) FROM battery) LIMIT 1'
        elif self == DataMode.Cameras:
            return 'select model FROM picam.cameras ORDER BY idx'
        elif self == DataMode.Modes:
            return 'select camera, model, format, width, height, fps from picam.modes join picam.cameras on camera=idx'
        else:
            raise Exception('No such operating mode')

    def single(self):
        return self == DataMode.Battery

    def autoClean(self):
        return self != DataMode.Battery

class DataStore:
    def __init__(self, database='picam', host='127.0.0.1', user='sql', password='sql'):
        self.db=MysqlStore(database,host,user,password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.db.close()

    @property
    def cameras(self):
        items = self.db.read(DataMode.Cameras)
        return [item[0] for item in items]

    @cameras.setter
    def cameras(self,cams):
        vals = ", ".join([f"({idx},'{cams[idx]}')" for idx in range(len(cams))])
        self.db.write(DataMode.Cameras,vals)

    @property
    def modes(self):
        raw = self.db.read(DataMode.Modes)
        return [PiCamInfo.fromTuple(row) for row in raw]

    @modes.setter
    def modes(self,modes):
        vals = ", ".join([modeMap(mode) for mode in modes])
        self.db.write(DataMode.Modes,vals)

    def json(self):
        interim = [mode.dict() for mode in self.modes]
        return json.dumps(interim)

    @property
    def battery(self):
        return self.db.read(DataMode.Battery)

    def batteryJSON(self):
        v, i, p = self.battery
        d = dict(voltage = v, current = i, percentage = p)
        return json.dumps(d)

    @battery.setter
    def battery(self, value):
        vals = f"({value.voltage}, {value.current}, {value.percentage})"
        self.db.write(DataMode.Battery, vals)

    def allBattery(self,origin=None):
        if origin is None:
            sql = 'SELECT timestamp, voltage, current, percentage FROM picam.battery ORDER BY timestamp'
        else:
           sql = f'SELECT timestamp, voltage, current, percentage FROM picam.battery WHERE timestamp >= FROM_UNIXTIME({origin}) ORDER BY timestamp'
        return self.db.select(sql)


