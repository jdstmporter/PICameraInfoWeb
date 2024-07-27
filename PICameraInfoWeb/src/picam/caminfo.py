import json

class PiCamModeInfo:

    def __init__(self,mode):
        self.format = mode['format'].format
        sz = mode['size']
        self.width = sz[0]
        self.height = sz[1]
        self.fps = mode['fps']

    def dict(self):
        return dict(
            format=self.format,
            width=self.width,
            height=self.height,
            fps=self.fps
        )

    def json(self):
        return json.dumps(self.dict)

class PiCamInfo:

    def __init__(self, index, model, modes):
        self.index = index
        self.model = model
        self.modes = [PiCamModeInfo(m) for m in modes]

    def dict(self):
        return dict(
            index=self.index,
            model=self.model,
            modes=[m.dict() for m in self.modes]
        )

    def json(self):
        return json.dumps(self.dict())



