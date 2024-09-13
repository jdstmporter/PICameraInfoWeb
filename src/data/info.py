import json


class PiCamInfo:
    def __init__(self, index, model, mode):
        self.index = index
        self.model = model
        self.format = mode.format
        self.width = mode.width
        self.height = mode.height
        self.fps = mode.fps

    @classmethod
    def fromTuple(cls,item):
        index = item[0]
        model = item[1]
        fmt = item[2]
        sz = (item[3], item[4])
        fps = item[5]
        mode = PiCamMode(format=fmt, size=sz, fps=fps)
        return PiCamInfo(index, model, mode)

    def __str__(self):
        return f'index: {self.index} [{self.model}], format: {self.format}, size: ({self.width}x{self.height}), fps: {self.fps} '

    def dict(self):
        return dict(
            index=self.index,
            model=self.model,
            format=self.format,
            width=self.width,
            height=self.height,
            fps=self.fps
        )

    def tuple(self):
        return tuple([self.index, self.format, self.width, self.height, self.fps])

    def json(self):
        return json.dumps(self.dict())

    def sql(self):
        return f"({', '.join(self.tuple())})"

class PiCamMode:
    def __init__(self, **mode):
        fmt = mode['format']
        if type(fmt) == str:
            self.format = fmt
        else:
            self.format = fmt.format


        size = mode['size']

        self.width = size[0]
        self.height = size[1]
        self.fps = mode['fps']

