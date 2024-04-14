from ..core import app_config

class ServiceDefinition(app_config.ServiceDefinitionProtocol):

    def __init__(self, class_name: type, lifetime: str) -> None:
        self._class_name: type = class_name
        self._lifetime: str = lifetime

    def class_name(self) -> type:
        return self._class_name

    def lifetime(self) -> str:
        return self._lifetime

class ContainerDefinition(app_config.ContainerDefinitionProtocol):
    
    def __init__(self) -> None:
        self._service_definitions: dict[type, ServiceDefinition] = dict()

    def singleton(self, service: type) -> ServiceDefinition:
        """Register a service with the singleton lifetime."""
        if service in self._service_definitions:
            raise ValueError(f'{service} was already registered')
        service_definition = ServiceDefinition(service, 'singleton')
        self._service_definitions[service] = service_definition
        return service_definition
    
    def scoped(self, service: type) -> ServiceDefinition:
        """Register a service with the scoped lifetime."""
        if service in self._service_definitions:
            raise ValueError(f'{service} was already registered')
        service_definition = ServiceDefinition(service, 'scoped')
        self._service_definitions[service] = service_definition
        return service_definition
    
    def transient(self, service: type) -> ServiceDefinition:
        """Register a service with the transient lifetime."""
        if service in self._service_definitions:
            raise ValueError(f'{service} was already registered')
        service_definition = ServiceDefinition(service, 'transient')
        self._service_definitions[service] = service_definition
        return service_definition

    def get_all_service_definitions(self) -> set[ServiceDefinition]:
        return set(self._service_definitions.values())

    def get_singleton_service_definitions(self) -> set[ServiceDefinition]:
        return set([d for d in self._service_definitions.values() if d.lifetime() == 'singleton'])
    
    def get_scoped_service_definitions(self) -> set[ServiceDefinition]:
        return set([d for d in self._service_definitions.values() if d.lifetime() == 'scoped'])

    def get_transient_service_definitions(self) -> set[ServiceDefinition]:
        return set([d for d in self._service_definitions.values() if d.lifetime() == 'transient'])
