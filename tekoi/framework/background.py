from tekoi.core import app_config

class BackgroundService(app_config.BackgroundService):
    pass


class BackgroundServiceDefinitionCollection:

    def __init__(self) -> None:
        self._background_service_definitions: list[app_config.BackgroundServiceDefinition] = []

    def add(self, cls: type[BackgroundService]) -> None:
        self._background_service_definitions.append(app_config.BackgroundServiceDefinition(cls))
