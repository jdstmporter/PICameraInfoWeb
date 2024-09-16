import traceback

from data import DataStore
from tools import UPSDevice, PiCam
import util

class ToolAction:
    def list(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def clean(self,**kwargs):
        pass

    def __call__(self,*args,**kwargs):
        action=kwargs['action']
        if action == 'raw':
            self.list()
        elif action == 'load':
            self.read()
        elif action == 'store':
            self.write()
        elif action == 'clean':
            self.clean()
        else:
            raise Exception(f'Unknown action {action} on tool processor')


class BatteryTool(ToolAction):
    def __init__(self):
        self.ups = UPSDevice()
        self.sql = DataStore()

    def __del__(self):
        self.sql.close()



    def list(self):
        try:
            #print(f'UPS[{self.ups}]')
            info = self.ups()
            print(str(info))
        except Exception as e:
            util.handle_error(e)


    def read(self):
        try:
            info = self.sql.all_battery()
            print('timestamp,voltage,current,percentage')
            for row in info:
                row_str = [str(i) for i in row]
                print(f"'{row_str[0]}',{row_str[1]},{row_str[2]},{row_str[3]}")
        except Exception as e:
            util.handle_error(e)

    def write(self):
        try:
            info = self.ups()
            self.sql.battery = info
        except Exception as e:
            util.handle_error(e)

    def clean(self,**kwargs):
        try:
            self.sql.clean_battery(**kwargs)
        except Exception as e:
            util.handle_error(e)


class CameraTool(ToolAction):
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
            util.handle_error(e)

    def read(self):
        try:
            CameraTool.dump(self.sql.cameras, self.sql.modes)
        except Exception as e:
            util.handle_error(e)

    def write(self):
        try:
            print('Initialising camera info database')
            print('Getting camera info')
            cameras, modes = self._info()
            CameraTool.dump(cameras, modes)

            print('Loading database : cameras')
            self.sql.cameras = cameras
            print('Loading database : modes')
            self.sql.modes = modes
        except Exception as e:
            util.handle_error(e)


