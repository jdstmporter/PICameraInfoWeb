from .caminfo import PiCamInfo
from .exists import isAvailable

if isAvailable('picamera2'):
    from .real import PiCamReal as PiCam
else:
    from .dummy import PiCamDummy as PiCam


