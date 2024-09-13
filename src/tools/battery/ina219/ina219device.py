import enum
import math
from util.i2c import I2CDevice

class Registers(enum.Enum):
    Configuration = 0
    ShuntVoltage = 1
    BusVoltage = 2
    Power = 3
    Current = 4
    Calibration = 5

class Mode(enum.Enum):
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
    def i_range(self):
        return math.pow(2.0,self._code) * 0.04

class ADC(BaseParameter):
    def __init__(self,code,bits,samples):
        super().__init__(code,(bits,samples))

    @property
    def n_bits(self):
        return self.value[0]

    @property
    def n_samples(self):
        return self.value[1]


class INA219Config:
    Range16V = VoltageRange(16, 0)
    Range32V = VoltageRange(32, 1)
    GainDiv1 = Gain(0)
    GainDiv2 = Gain(1)
    GainDiv4 = Gain(2)
    GainDiv8 = Gain(3)
    ADC9Bit = ADC(0, 9, 1)
    ADC10Bit = ADC(1, 10, 1)
    ADC11Bit = ADC(2, 11, 1)
    ADC12Bit = ADC(3, 12, 1)
    ADC12Bit2 = ADC(9, 12, 2)
    ADC12Bit4 = ADC(10, 12, 4)
    ADC12Bit8 = ADC(11, 12, 8)
    ADC12Bit16 = ADC(12, 12, 16)
    ADC12Bit32 = ADC(13, 12, 32)
    ADC12Bit64 = ADC(14, 12, 64)
    ADC12Bit128 = ADC(15, 12, 128)

    def __init__(self,*args,**kwargs):
        pass

class Settings:
    def __init__(self,v_range = INA219Config.Range16V, gain = INA219Config.GainDiv2, adc = INA219Config.ADC12Bit32, mode = Mode.ShuntAndBusContinuous):
        self.vRange = v_range
        self.gain = gain
        self.adc = adc
        self.mode = mode

    def __call__(self):
        adc = self.adc()
        return (self.vRange()<<13) | (self.gain() << 11) | (adc << 7) | (adc << 3) | self.mode.value

    @property
    def maxVoltage(self):
        return self.vRange.value

class INA219:

    register_keys = dict(
        shunt_voltage = Registers.ShuntVoltage,
        bus_voltage = Registers.BusVoltage,
        current = Registers.Current,
        power = Registers.Power
    )

    def __init__(self, bus = 1, address = 0x40, max_expected_current=1,rShunt=0.01):
        self.i2c = I2CDevice(bus=bus, address=address)

        current_lsb = max_expected_current / 32768
        self.rShunt = rShunt
        self.calibratedValue = int(0.04096 / (current_lsb * self.rShunt))

        self.lsb = dict()
        self.lsb[Registers.BusVoltage] = 0.004
        self.lsb[Registers.ShuntVoltage] = 0.01
        self.lsb[Registers.Current] = current_lsb
        self.lsb[Registers.Power] = 20.0 * current_lsb

    def _read(self,register):
        return self.i2c.read16(register.value)

    def _write(self,register,value):
        self.i2c.write16(register.value,value)

    def _decode(self,register,value):
        lsb = self.lsb[register]
        if register == Registers.BusVoltage:
            return (value>>3) * lsb
        else:
            add = 0 if value > 0 else 65535
            return (value + add) * lsb

    def __getattr__(self,key):
        register = self.register_keys[key]
        value = self._read(register)
        return self._decode(register,value)

    def configure(self,config):
        self._write(Registers.Configuration,config)

    def calibrate(self):
        self._write(Registers.Calibration, self.calibratedValue)












