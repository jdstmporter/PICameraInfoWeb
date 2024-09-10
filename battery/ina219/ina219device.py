from enum import Enum
import math



class Registers(Enum):
    Configuration = 0
    ShuntVoltage = 1
    BusVoltage = 2
    Power = 3
    Current = 4
    Calibration = 5

class Mode(Enum):
    PowerDown = 0x00  # power down
    ShuntTriggered = 0x01  # shunt voltage triggered
    BusTriggered = 0x02  # bus voltage triggered
    ShuntAndBusTriggered = 0x03  # shunt and bus voltage triggered
    ADCOff = 0x04  # ADC off
    ShuntContinuous = 0x05  # shunt voltage continuous
    BusContinuous = 0x06  # bus voltage continuous
    ShuntAndBusContinuous = 0x07  # shunt and bus voltage continuous

class BaseParameter:
    def __init__(self, code, value):
        self._code=code
        self._value=value

    @property
    def value(self):
        return self._value

    def __call__(self):
        return self._code


class VoltageRange(BaseParameter):
    pass


class Gain(BaseParameter):
    def __init__(self,code):
        super().__init__(code,None)

    @property
    def iRange(self):
        return math.pow(2.0,self._code) * 0.04

class ADC(BaseParameter):
    def __init__(self,code,bits,samples):
        super().__init__(code,(bits,samples))

    @property
    def nBits(self):
        return self.value[0]

    @property
    def nSamples(self):
        return self.value[1]




