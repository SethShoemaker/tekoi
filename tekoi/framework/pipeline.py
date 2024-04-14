from ..core import app_config
from . import request, response

class PipelineMember(app_config.PipelineMemberProtocol):

    def __call__(self, request: request.Request, next: callable) -> response.Response:
        pass


class PipelineMemberDefinition(app_config.PipelineMemberDefinitionProtocol):

    def __init__(self, class_name: type[PipelineMember], lifetime: str) -> None:
        self._class_name = class_name
        self._lifetime = lifetime

    def class_name(self) -> type[PipelineMember]:
        return self._class_name

    def lifetime(self) -> str:
        return self._lifetime


class PipelineDefinition(app_config.PipelineDefinitionProtocol):

    def __init__(self) -> None:
        self._pipeline_member_definitions: list[PipelineMemberDefinition] = []

    def singleton(self, class_name: type[PipelineMember]) -> PipelineMemberDefinition:
        definition = PipelineMemberDefinition(class_name=class_name, lifetime="singleton")
        self._pipeline_member_definitions.append(definition)
        return definition
    
    def scoped(self, class_name: type[PipelineMember]) -> PipelineMemberDefinition:
        definition = PipelineMemberDefinition(class_name=class_name, lifetime="scoped")
        self._pipeline_member_definitions.append(definition)
        return definition
    
    def get_members(self) -> list[PipelineMemberDefinition]:
        return self._pipeline_member_definitions
