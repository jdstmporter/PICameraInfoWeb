from util import Logger
from .ina219 import Registers, Settings, LSB
from .i2c import I2CDevice



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
        self.i2c = I2CDevice(bus=bus,address=address)
        self.settings = settings
        self.lsb = LSB(max_expected_current,0.01)


    def connect(self):
        Logger.log.info('Connecting to UPS device')
        self.i2c.write16(Registers.Configuration.value,self.settings())
        self.calibrate()

    def close(self):
        pass
        

    def calibrate(self):
        self.i2c.write16(Registers.Calibration.value, self.lsb.calibratedValue)

    @classmethod
    def _decode_value(cls, value, scale = 0.01):
        add = 0 if value > 0 else 65535
        return(value+add)*scale

    @property
    def shunt_voltage(self):
        self.calibrate()
        value = self.i2c.read16(Registers.ShuntVoltage.value)
        return self._decode_value(value, scale=self.lsb.shuntLSB)

    @property
    def bus_voltage(self):
        self.calibrate()
        self.i2c.read16(Registers.BusVoltage.value)
        value = self.i2c.read16(Registers.BusVoltage.value)
        #value = self.__read(Registers.BusVoltage)
        return (value>>3) * self.lsb.busLSB

    @property
    def current(self):
        self.calibrate()
        #return self.shuntVoltage()*self.lsb.calibratedValue/4096
        self.i2c.read16(Registers.Current.value)
        value = self.i2c.read16(Registers.Current.value)
        return self._decode_value(value, scale=self.lsb.currentLSB)


    @property
    def power(self):
        self.calibrate()
        value = self.i2c.read16(Registers.Power.value)
        return self._decode_value(value, scale=self.lsb.powerLSB)


    def __call__(self):
        return UPSInfo(voltage=self.bus_voltage, current=self.current)





