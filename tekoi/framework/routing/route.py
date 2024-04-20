from tekoi.framework import PipelineMember

class Route:

    def __init__(self, method: str = None, path: str = None, cls: type[PipelineMember] = None) -> None:
        self.method = method
        self.path = path
        self.cls = cls
