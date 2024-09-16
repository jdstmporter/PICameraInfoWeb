import util
from .ina219 import INA219, Settings

class UPSInfo:
    def __init__(self,voltage = 0.0,current = 0.0,timestamp = None):
        self.voltage = round(voltage,3)
        self.current = round(current,6)
        self.timestamp = timestamp

    @property
    def percentage(self):
        p = (self.voltage - 3) / 1.2 * 100
        return round(max([0.0, min([p, 100.0])]),2)

    def __iter__(self):
        return iter([self.voltage, self.current, self.percentage])

    def __str__(self):
        return f'Load = {self.voltage}V, current = {self.current*1000}mA, percentage = {self.percentage}%'


class UPSDevice:

    def __init__(self,bus = 1, address = 0x43,settings = Settings(),max_expected_current = 5.0):
        self.ina219 = INA219(bus=bus,address=address,max_expected_current = max_expected_current)
        self.config = settings()

    def connect(self):
        util.Logger.log.info('Connecting to UPS device')
        self.ina219.configure(self.config)
        self.ina219.calibrate()

    def close(self):
        pass

    @property
    def shunt_voltage(self):
        self.ina219.calibrate()
        return self.ina219.shunt_voltage()

    @property
    def bus_voltage(self):
        self.ina219.calibrate()
        self.ina219.bus_voltage()
        return self.ina219.bus_voltage()

    @property
    def current(self):
        self.ina219.calibrate()
        self.ina219.current()
        return self.ina219.current()

    @property
    def power(self):
        self.ina219.calibrate()
        self.ina219.power()
        return self.ina219.power()

    def __call__(self):
        return UPSInfo(voltage=self.bus_voltage, current=self.current)






