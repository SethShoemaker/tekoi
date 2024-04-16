from abc import ABC as _ABC
from typing import Protocol as _Protocol
from .request import Request as _Request
from .response import Response as _Response


class PipelineMemberProtocol(_Protocol):
    
    def __call__(self, request: _Request, next: callable) -> _Response:
        pass


class PipelineMemberDefinition(_ABC):
    pass


class SingletonPipelineMemberDefinition(PipelineMemberDefinition, _ABC):
    pass


class RegisteredSingletonPipelineMemberDefinition(SingletonPipelineMemberDefinition):

    def __init__(self, cls: type[PipelineMemberProtocol]) -> None:
        self.cls = cls


class BindedSingletonPipelineMemberDefinition(SingletonPipelineMemberDefinition):

    def __init__(self, instance: PipelineMemberProtocol) -> None:
        self.instance = instance


class ScopedPipelineMemberDefinition(PipelineMemberDefinition, _ABC):
    pass


class RegisteredScopedPipelineMemberDefinition(ScopedPipelineMemberDefinition):
    
    def __init__(self, cls: type[PipelineMemberProtocol]) -> None:
        self.cls = cls
