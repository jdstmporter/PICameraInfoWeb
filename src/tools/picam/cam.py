from picamera2 import Picamera2
from tools.data import PiCamInfo, PiCamMode
import json



class PiCam:
    def __init__(self):
        cams = Picamera2.global_camera_info()
        self.cams = [c['Model'] for c in cams]



    def __camera(self, index):
        camera = Picamera2(index)
        modes = camera.sensor_modes
        return [PiCamInfo(index, self.cams[index], PiCamMode(**mode)) for mode in modes]

    def __call__(self):
        n = len(self.cams)
        out = [[info.dict() for info in self.__camera(index)] for index in range(0, n)]
        return json.dumps(out)

    @property
    def cameras(self):
        return self.cams

    @property
    def modes(self):
        n = len(self.cams)
        out=[]
        for index in range(0,n):
            out.extend(self.__camera(index))
        return out






