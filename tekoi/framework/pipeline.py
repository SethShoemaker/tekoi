from tekoi.core import startup as _startup
import abc
import typing
from .request import Request as _Request
from .response import Response as _Response
from .builder import AppBuilder as _AppBuilder


class PipelineMember(_startup.PipelineMemberProtocol):

    @abc.abstractmethod
    def __call__(self, request: _Request, next: typing.Callable[[_Request], _Response]) -> _Response:
        pass


class PipelineMemberDefinitionCollection:

    def __init__(self, builder: _AppBuilder) -> None:
        self._builder = builder
        self._pipeline_member_definitions: list[_startup.PipelineMemberDefinition] = []

    def register_singleton(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(_startup.RegisteredSingletonPipelineMemberDefinition(member))

    def bind_singleton(self, member: PipelineMember) -> None:
        self._pipeline_member_definitions.append(_startup.BindedSingletonPipelineMemberDefinition(member))

    def register_scoped(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(_startup.RegisteredScopedPipelineMemberDefinition(member))

    def register_exception_handler_singleton(self) -> None:
        from . import exception_handling as _exception_handling
        self._pipeline_member_definitions.append(_startup.RegisteredSingletonPipelineMemberDefinition(_exception_handling.Handler))

    def bind_router_singleton(self) -> None:
        from . import routing as _routing
        self._pipeline_member_definitions.append(_startup.BindedSingletonPipelineMemberDefinition(_routing.Router(self._builder.routing.routes)))

    def register_routing_handler_singleton(self) -> None:
        from . import routing as _routing
        self._pipeline_member_definitions.append(_startup.RegisteredScopedPipelineMemberDefinition(_routing.Handler))
