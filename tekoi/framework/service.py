from tekoi.core import app_config

class ServiceDefinitionCollection:
    
    def __init__(self) -> None:
        self._service_definitions: list[app_config.ServiceDefinition] = []

    def register_singleton(self, service: type) -> None:
        self._service_definitions.append(app_config.RegisteredSingletonServiceDefinition(service))
    
    def bind_singleton(self, service: object) -> None:
        self._service_definitions.append(app_config.BindedSingletonServiceDefinition(service))

    def register_scoped(self, service: type) -> None:
        self._service_definitions.append(app_config.RegisteredScopedServiceDefinition(service))

    def register_transient(self, service: type) -> None:
        self._service_definitions.append(app_config.RegisteredTransientServiceDefinition(service))
