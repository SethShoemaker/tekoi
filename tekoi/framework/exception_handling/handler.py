from typing import Callable as _Callable
from tekoi.framework import (PipelineMember as _PipelineMember, 
                             Request as _Request, 
                             Response as _Response,
                             internal_server_error as _internal_server_error)


class Handler(_PipelineMember):

    def __init__(self) -> None:
        pass

    def __call__(self, request: _Request, next: _Callable[[_Request], _Response]) -> _Response:
        try:
            res = next(request)
            return res
        except Exception as e:
            return _internal_server_error(bytes())
