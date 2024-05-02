from abc import ABC as _ABC


class ServiceDefinition(_ABC):
    pass


class SingletonServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredSingletonServiceDefinition(SingletonServiceDefinition):

    def __init__(self, interface: type, implementation: type) -> None:
        self.interface = interface
        self.implementation = implementation


class BindedSingletonServiceDefinition(SingletonServiceDefinition):

    def __init__(self, interface: type, instance: object) -> None:
        self.interface = interface
        self.instance = instance


class ScopedServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredScopedServiceDefinition(ScopedServiceDefinition):

    def __init__(self, interface: type, implementation: type) -> None:
        self.interface = interface
        self.implementation = implementation


class TransientServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredTransientServiceDefinition(TransientServiceDefinition):

    def __init__(self, interface: type, implementation: type) -> None:
        self.interface = interface
        self.implementation = implementation
