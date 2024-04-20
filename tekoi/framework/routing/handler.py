from tekoi.core import app_config, services
from tekoi.framework import Request, Response
from .router import Router

class Handler(app_config.PipelineMemberProtocol):

    def __init__(self, router: Router, scoped_container: services.ScopedContainer):
        self._router = router
        self.scoped_container = scoped_container

    def __call__(self, request: Request, next: callable) -> Response:
        if request.routing_target is None:
            return next(request)
        
        target_instance = self.scoped_container.resolve_scoped_service(request.routing_target)
        next = (lambda target_instance, next: lambda request: target_instance(request, next))(target_instance, next)
        return next(request)
