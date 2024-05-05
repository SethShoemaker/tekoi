from tekoi.core import startup as _startup
from .builder import AppBuilder as _AppBuilder

class BackgroundService(_startup.BackgroundService):
    pass


class BackgroundServiceDefinitionCollection:

    def __init__(self, builder: _AppBuilder) -> None:
        self._builder = builder
        self._background_service_definitions: list[_startup.BackgroundServiceDefinition] = []

    def add(self, cls: type[BackgroundService]) -> None:
        self._background_service_definitions.append(_startup.BackgroundServiceDefinition(cls))
