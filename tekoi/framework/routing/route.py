from tekoi.framework import PipelineMember

class Route:
    
    method: str|None = None
    path: str|None = None
    cls: type[PipelineMember] = None
