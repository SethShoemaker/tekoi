from . import pipeline, service, background
from tekoi import core

class AppBuilder:

    def __init__(self) -> None:
        self.services: service.ServiceDefinitionCollection = service.ServiceDefinitionCollection()
        self.pipeline: pipeline.PipelineMemberDefinitionCollection = pipeline.PipelineMemberDefinitionCollection()
        self.request_class: type[pipeline.Request] = pipeline.Request
        self.response_class: type[pipeline.Response] = pipeline.Response
        self.background_services: background.BackgroundServiceDefinitionCollection = background.BackgroundServiceDefinitionCollection() 

    def build(self) -> core.App:
        return core.App(
            request_class=self.request_class,
            response_class=self.response_class,
            service_definitions=self.services._service_definitions,
            pipeline_member_definitions=self.pipeline._pipeline_member_definitions,
            background_service_definitions=self.background_services._background_service_definitions
        )
