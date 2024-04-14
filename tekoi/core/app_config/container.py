from typing import Protocol


class ServiceDefinitionProtocol(Protocol):
    
    def class_name(self) -> type:
        pass

    def lifetime(self) -> str:
        pass


class ContainerDefinitionProtocol(Protocol):

    def get_all_service_definitions(self) -> set[ServiceDefinitionProtocol]:
        pass

    def get_singleton_service_definitions(self) -> set[ServiceDefinitionProtocol]:
        pass
    
    def get_scoped_service_definitions(self) -> set[ServiceDefinitionProtocol]:
        pass
    
    def get_transient_service_definitions(self) -> set[ServiceDefinitionProtocol]:
        pass
