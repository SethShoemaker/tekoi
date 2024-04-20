from tekoi.framework import PipelineMember as _PipelineMember

class Route:

    def __init__(self, method: str, path: str, cls: type[_PipelineMember]) -> None:
        self.method = method
        self.path = path
        self.cls = cls
