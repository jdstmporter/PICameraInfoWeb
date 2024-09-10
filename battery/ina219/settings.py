from .ina219device import VoltageRange, Gain, ADC, Mode

class Config:
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
    def __init__(self,v_range = Config.Range16V, gain = Config.GainDiv2, adc = Config.ADC12Bit32, mode = Mode.ShuntAndBusContinuous):
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

class LSB:
    def __init__(self,maximumExpectedCurrent=1,rShunt=0.01):
        self.rShunt = rShunt
        self.busLSB = 0.004
        self.shuntLSB = 0.01
        self.currentLSB = maximumExpectedCurrent / 32768
        self.powerLSB = 20.0 * self.currentLSB

        self.calibratedValue = int(0.04096 / (self.currentLSB * self.rShunt))
