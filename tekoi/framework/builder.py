from . import pipeline, request, response, service
from ..core import App

class AppBuilder:

    def __init__(self) -> None:
        self.services: service.ContainerDefinition = service.ContainerDefinition()
        self.pipeline: pipeline.PipelineDefinition = pipeline.PipelineDefinition()
        self.request_class: type[request.Request] = request.Request
        self.response_class: type[response.Response] = response.Response

    def build(self) -> App:
        return App(
            request_class=self.request_class,
            response_class=self.response_class,
            container_definition=self.services,
            pipeline_definition=self.pipeline
        )
