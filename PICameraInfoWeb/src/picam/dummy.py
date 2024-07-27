from .caminfo import PiCamInfo
import json



class DummyFormat:
        def __init__(self,format):
            self.format=format

class PiCamDummy:

    KIND = 'DUMMY'

    def __init__(self):
        self.cams=['dummy']
    
    def __camera(self,index):
        modes = [{
            'format' : DummyFormat('dummyformat'),
            'size' : [1920,1680],
            'fps'  : 50
        }]
        return [PiCamInfo(0,'dummyCamera',modes)]
    
    def __call__(self):
        n = len(self.cams)
        out = [[info.dict() for info in self.__camera(index)] for index in range(0, n)]
        return json.dumps(out)


    