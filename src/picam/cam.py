from picamera2 import Picamera2
import json



class PiCamInfo:

    def __init__(self, index, model, mode):
        self.index = index
        self.model = model
        self.format = mode['format'].format
        sz = mode['size']
        self.width = sz[0]
        self.height = sz[1]
        self.fps = mode['fps']

    def dict(self):
        return dict(
            index=self.index,
            model=self.model,
            format=self.format,
            width=self.width,
            height=self.height,
            fps=self.fps
        )

    def json(self):
        return json.dumps(self.dict())


class PiCam:
    def __init__(self):
        cams = Picamera2.global_camera_info()
        self.cams = [c['Model'] for c in cams]

    def __camera(self, index):
        camera = Picamera2(index)
        modes = camera.sensor_modes
        return [PiCamInfo(index, self.cams[index], mode) for mode in modes]

    def __call__(self):
        n = len(self.cams)
        out = [[info.dict() for info in self.__camera(index)] for index in range(0, n)]
        return json.dumps(out)




