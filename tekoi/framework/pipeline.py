from ..core import app_config
from . import request, response

class PipelineMember(app_config.PipelineMemberProtocol):

    def __call__(self, request: request.Request, next: callable) -> response.Response:
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
