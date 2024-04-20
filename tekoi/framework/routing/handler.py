from tekoi import core as _core
from tekoi.framework import (Request as _Request,
                             Response as _Response, 
                             PipelineMember as _PipelineMember)
from .router import Router as _Router
import typing as _typing

class Handler(_PipelineMember):

    def __init__(self, router: _Router, scoped_container: _core.ScopedContainer):
        self._router = router
        self.scoped_container = scoped_container

    def __call__(self, request: _Request, next: _typing.Callable) -> _Response:
        if request.routing_target is None:
            return next(request)
        
        target_instance = self.scoped_container.resolve_scoped_service(request.routing_target)
        if not isinstance(target_instance, _PipelineMember):
            raise TypeError("The routing_target type set in the request is not derived from PipelineMember")
        next = (lambda target_instance, next: lambda request: target_instance(request, next))(target_instance, next)
        return next(request)
