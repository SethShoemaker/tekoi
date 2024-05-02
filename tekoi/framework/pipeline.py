from tekoi.core import startup as _startup
import abc
import typing

class Request(_startup.Request):

    routing_target = None

    routing_path_params: dict[str, str]| None = None

    sessions_session_data = None


class Response(_startup.Response):
    pass


class PipelineMember(_startup.PipelineMemberProtocol):

    @abc.abstractmethod
    def __call__(self, request: Request, next: typing.Callable[[Request], Response]) -> Response:
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
