from tekoi.core import app_config
import abc
import typing

class Request(app_config.Request):

    routing_target: type[PipelineMember]|None = None

    path_params: dict[str, str]| None = None


class Response(app_config.Response):
    pass


class PipelineMember(app_config.PipelineMemberProtocol):

    @abc.abstractmethod
    def __call__(self, request: Request, next: typing.Callable) -> Response:
        pass


class PipelineMemberDefinitionCollection:

    def __init__(self) -> None:
        self._pipeline_member_definitions: list[app_config.PipelineMemberDefinition] = []

    def register_singleton(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(app_config.RegisteredSingletonPipelineMemberDefinition(member))

    def bind_singleton(self, member: PipelineMember) -> None:
        self._pipeline_member_definitions.append(app_config.BindedSingletonPipelineMemberDefinition(member))

    def register_scoped(self, member: type[PipelineMember]) -> None:
        self._pipeline_member_definitions.append(app_config.RegisteredScopedPipelineMemberDefinition(member))
