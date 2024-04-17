from tekoi.core import app_config

class Request(app_config.Request):

    routing_target: type[app_config.PipelineMemberProtocol]|None = None
