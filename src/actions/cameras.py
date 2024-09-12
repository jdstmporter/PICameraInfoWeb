
from data import DataStore
from tools import UPSDevice, PiCam

class ToolAction:


    def list(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def __call__(self,*args,**kwargs):
        action=kwargs['action']
        if action == 'raw':
            self.list()
        elif action == 'load':
            self.read()
        elif action == 'store':
            self.write()
        else:
            raise Exception(f'Unknown action {action} on tool processor')


class Battery(ToolAction):
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




class Cameras(ToolAction):
    def __init__(self):
        self.cams = PiCam()
        self.sql = DataStore()

    def __del__(self):
            self.sql.close()

    def _info(self):
        return [self.cams.cameras, self.cams.modes]

    @classmethod
    def dump(cls,cams, mods):
        print('Cameras:')
        for n in range(len(cams)):
            print(f'{n} : {cams[n]}')
        print('Modes:')
        for mode in mods:
            print(str(mode))


    def list(self):
        try:
            cameras, modes = self._info()
            self.dump(cameras, modes)
        except Exception as e:
            print(f'Error : {e}')

    def read(self):
        try:
            Cameras.dump(self.sql.cameras, self.sql.modes)
        except Exception as e:
            print(f'Error : {e}')

    def write(self):
        try:
            print('Initialising camera info database')
            print('Getting camera info')
            cameras, modes = self._info()
            Cameras.dump(cameras, modes)

            print('Loading database')
            self.sql.cameras = cameras
            self.sql.modes = modes
        except Exception as e:
            print(f'Error: {e}')


