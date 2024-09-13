import operator
from functools import reduce
import smbus2

import util


class I2CDevice:
    def __init__(self,bus=1,address=0x00):
        self.bus=bus
        self.address=address
        self.i2c = smbus2.SMBus(bus)

    def __del__(self):
        try:
            self.i2c.close()
        except Exception as e:
            util.Logger.log.error(f'Error closing i2c: {e}')


    @classmethod
    def _int2bytes(cls,value,n=4):
        values = [(value>>(8*b))&0xff for b in range(n)]
        values.reverse()
        return values

    @ classmethod
    def _bytes2int(cls,data=None):
        if data is None:
            data=[]
        data.reverse()
        return reduce(operator.or_,[data[b]<<(8*b) for b in range(len(data))])

    def read(self,register,nbytes=4):
        values = self.i2c.read_i2c_block_data(self.address, register, nbytes)
        return self._bytes2int(values)

    def write(self,register,data,nbytes=4):
        values = self._int2bytes(data,nbytes)
        self.i2c.write_i2c_block_data(self.address,register,values)

    def read8(self,register):
        return self.i2c.read_byte_data(self.address,register)

    def write8(self,register,data):
        self.i2c.write_byte_data(self.address,register,data)

    def read16(self,register):
        return self.read(register,2)

    def write16(self,register,word):
        self.write(register,word,2)









