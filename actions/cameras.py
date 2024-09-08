from data import DataStore
from picam import PiCam

class Cameras:

    def __init__(self):
        self.cams = PiCam()
        self.sql = DataStore()

    def __del__(self):
            self.sql.close()

    def __call__(self):
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
            cameras, modes = self()
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
            cameras, modes = Cameras()()
            Cameras.dump(cameras, modes)

            print('Loading database')
            self.sql.cameras = cameras
            self.sql.modes = modes
        except Exception as e:
            print(f'Error: {e}')


