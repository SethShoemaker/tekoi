from tekoi.core import startup as _startup

class ServiceDefinitionCollection:
    
    def __init__(self) -> None:
        self._service_definitions: list[_startup.ServiceDefinition] = []

    def register_singleton(self, interface: type, implementation: type) -> None:
        self._service_definitions.append(_startup.RegisteredSingletonServiceDefinition(interface, implementation))
    
    def bind_singleton(self, interface: type, instance: object) -> None:
        self._service_definitions.append(_startup.BindedSingletonServiceDefinition(interface, instance))

    def register_scoped(self, interface: type, implementation: type) -> None:
        self._service_definitions.append(_startup.RegisteredScopedServiceDefinition(interface, implementation))

    def register_transient(self, interface: type, implementation: type) -> None:
        self._service_definitions.append(_startup.RegisteredTransientServiceDefinition(interface, implementation))
