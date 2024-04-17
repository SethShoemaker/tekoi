from tekoi.core import app_config
from tekoi.framework.routing import Route

class Router(app_config.PipelineMemberProtocol):

    def __init__(
            self,
            routes: list[Route]
        ):
        self.routes = routes

    def __call__(self, request: app_config.Request, next: callable) -> app_config.Response:
        print(request.path)
        return next(request)
