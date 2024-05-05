from tekoi import core as _core

class AppBuilder:

    def __init__(self) -> None:
        from .request import Request as _Request
        self.request_class: type[_Request] = _Request

        from .response import Response as _Response
        self.response_class: type[_Response] = _Response

        from .service import ServiceDefinitionCollection as _ServiceDefinitionCollection
        self.services: _ServiceDefinitionCollection = _ServiceDefinitionCollection(self)

        from .pipeline import PipelineMemberDefinitionCollection as _PipelineMemberDefinitionCollection
        self.pipeline: _PipelineMemberDefinitionCollection = _PipelineMemberDefinitionCollection(self)

        from .background import BackgroundServiceDefinitionCollection as _BackgroundServiceDefinitionCollection
        self.background_services: _BackgroundServiceDefinitionCollection = _BackgroundServiceDefinitionCollection(self)
        
        from .routing import RoutingDefinition as _RoutingDefinition
        self.routing = _RoutingDefinition(self)

        from .sessions import SessionsDefinition as _SessionsDefinition
        self.sessions = _SessionsDefinition(self)

    def build(self) -> _core.App:
        return _core.App(
            request_class=self.request_class,
            response_class=self.response_class,
            service_definitions=self.services._service_definitions,
            pipeline_member_definitions=self.pipeline._pipeline_member_definitions,
            background_service_definitions=self.background_services._background_service_definitions
        )
