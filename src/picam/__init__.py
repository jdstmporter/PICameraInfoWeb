from .caminfo import PiCamInfo


from sys import modules
if 'PiCamera2' in modules.keys():
    from .real import PiCamReal as PiCam
else:
    from .dummy import PiCamDummy as PiCam


