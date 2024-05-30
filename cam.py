from flask import Flask, abort
from picamera2 import Picamera2


class Interrogate:

    def __init__(self, index=0):
        self.camera = Picamera2(index)

    def __call__(self):
        modes = self.camera.sensor_modes
        outputs = []
        for mode in modes:
            item = {
                'format': mode['format'],
                'width': mode['size'][0],
                'height': mode['size'][1],
                'fps': mode['fps']
            }
            outputs.append(item)
        return outputs

    @classmethod
    def cameras(cls):
        cams = Picamera2.global_camera_info()
        return [{'model': c['Model']} for c in cams]


app = Flask(__name__)
cameras = Interrogate()


@app.route('/cameras', methods=['GET'])
def cameraInfo():
    try:
        return Interrogate.cameras()
    except:
        abort(500)


@app.route('/modes', methods=['GET'])
def cameraMode():
    try:
        return cameras()
    except:
        abort(500)