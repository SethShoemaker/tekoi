from .background import BackgroundServiceDefinitionCollection as _BackgroundServiceDefinitionCollection
from .service import ServiceDefinitionCollection as _ServiceDefinitionCollection
from .pipeline import PipelineMemberDefinitionCollection as _PipelineMemberDefinitionCollection
from .request import Request as _Request
from .response import Response as _Response
from tekoi import core as _core

class AppBuilder:

    def __init__(self) -> None:
        self.services: _ServiceDefinitionCollection = _ServiceDefinitionCollection()
        self.pipeline: _PipelineMemberDefinitionCollection = _PipelineMemberDefinitionCollection()
        self.request_class: type[_Request] = _Request
        self.response_class: type[_Response] = _Response
        self.background_services: _BackgroundServiceDefinitionCollection = _BackgroundServiceDefinitionCollection() 

    def build(self) -> _core.App:
        return _core.App(
            request_class=self.request_class,
            response_class=self.response_class,
            service_definitions=self.services._service_definitions,
            pipeline_member_definitions=self.pipeline._pipeline_member_definitions,
            background_service_definitions=self.background_services._background_service_definitions
        )
