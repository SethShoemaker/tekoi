from tekoi.core import app_config

class Handler(app_config.PipelineMemberProtocol):

    def __call__(self, request: app_config.Request, next: callable) -> app_config.Response:
        return next(request)
