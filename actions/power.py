from time import sleep

from battery import UPSDevice
from data import DataStore

class Battery:
    def __init__(self):
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



class BatteryDaemon:
    def __init__(self,interval=10.0):
        self.interval=interval
        self.sql = DataStore()
        self.ups = UPSDevice()
        self.ups.connect()

    def __del__(self):
        self.ups.close()
        self.sql.close()

    def __call__(self):
        try:
            info = self.ups()
            print(str(info))
        except Exception as e:
            print(f'Error = {e}')

    def start(self):
        run = True
        while run:
            try:
                info = self.ups()
                self.sql.battery=info
                sleep(self.interval)
            except KeyboardInterrupt:
                print('Keyboard interrupt: terminating')
                run = False
            except Exception as e:
                print(f'Error : {e}')


