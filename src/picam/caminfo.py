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