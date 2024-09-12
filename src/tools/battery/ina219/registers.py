from enum import Enum

class Registers(Enum):
    Configuration = 0
    ShuntVoltage = 1
    BusVoltage = 2
    Power = 3
    Current = 4
    Calibration = 5