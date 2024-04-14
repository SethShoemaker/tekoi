from typing import Protocol
from .request import Request
from .response import Response


class PipelineMemberProtocol(Protocol):
    
    def __call__(self, request: Request, next: callable) -> Response:
        pass


class PipelineMemberDefinitionProtocol(Protocol):

    def class_name() -> type[PipelineMemberProtocol]:
        pass

    def lifetime() -> str:
        pass


class PipelineDefinitionProtocol(Protocol):

    def get_members(self) -> list[PipelineMemberDefinitionProtocol]:
        pass
