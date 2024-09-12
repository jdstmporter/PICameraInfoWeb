from time import sleep

from .base import BaseAction, ToolAction
from tools.battery import UPSDevice
from tools.data import DataStore
from tools.util import Logger


class Battery(ToolAction):
    def __init__(self):
        super().__init__('battery')
        self.ups=UPSDevice()
        self.sql = DataStore()

    def __del__(self):
        self.sql.close()



    def list(self):
        try:
            info = self.ups()
            print(str(info))
        except Exception as e:
            print(f'Error = {e}')

    def read(self):
        pass

    def write(self):
        try:
            info = self.ups()
            self.sql.battery = info
        except Exception as e:
            print(f'Error: {e}')



class BatteryDaemon(BaseAction):
    def __init__(self,interval=10):
        super().__init__()
        self.interval=interval
        self.sql = DataStore()
        self.ups = UPSDevice()
        self.ups.connect()

    def __del__(self):
        self.ups.close()
        self.sql.close()

    def __call__(self,**kwargs):
        run = True
        while run:
            try:
                info = self.ups()
                self.sql.battery=info
                sleep(self.interval)
            except KeyboardInterrupt:
                Logger.log.warning('Keyboard interrupt: terminating')
                run = False
            except Exception as e:
                Logger.log.error(f'Error : {e}')


