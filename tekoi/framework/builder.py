from . import pipeline, request, response, service
from tekoi import core

class AppBuilder:

    def __init__(self) -> None:
        self.services: service.ServiceDefinitionCollection = service.ServiceDefinitionCollection()
        self.pipeline: pipeline.PipelineMemberDefinitionCollection = pipeline.PipelineMemberDefinitionCollection()
        self.request_class: type[request.Request] = request.Request
        self.response_class: type[response.Response] = response.Response

    def build(self) -> core.App:
        return core.App(
            request_class=self.request_class,
            response_class=self.response_class,
            service_definitions=self.services._service_definitions,
            pipeline_member_definitions=self.pipeline._pipeline_member_definitions
        )
