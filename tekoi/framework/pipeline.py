from tekoi.core import startup as _startup
import abc
import typing
from .request import Request as _Request
from .response import Response as _Response


class PipelineMember(_startup.PipelineMemberProtocol):

    @abc.abstractmethod
    def __call__(self, request: _Request, next: typing.Callable[[_Request], _Response]) -> _Response:
        pass


class PipelineMemberDefinitionCollection:

    def __init__(self) -> None:
        self._pipeline_member_definitions: list[_startup.PipelineMemberDefinition] = []

    def register_singleton(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(_startup.RegisteredSingletonPipelineMemberDefinition(member))

    def bind_singleton(self, member: PipelineMember) -> None:
        self._pipeline_member_definitions.append(_startup.BindedSingletonPipelineMemberDefinition(member))

    def register_scoped(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(_startup.RegisteredScopedPipelineMemberDefinition(member))
