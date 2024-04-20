from tekoi.core import app_config, services
from tekoi.framework import Request, Response

class Handler(app_config.PipelineMemberProtocol):

    def __init__(self, service_facade: services.ScopedContainer) -> None:
        self.service_facade = service_facade

    def __call__(self, request: Request, next: callable) -> Response:
        if(request.routing_target):
            print(request.routing_target.cls)
        return next(request)
