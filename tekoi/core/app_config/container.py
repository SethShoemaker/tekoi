from abc import ABC as _ABC


class ServiceDefinition(_ABC):
    pass


class SingletonServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredSingletonServiceDefinition(SingletonServiceDefinition):

    def __init__(self, cls: type) -> None:
        self.cls = cls


class BindedSingletonServiceDefinition(SingletonServiceDefinition):

    def __init__(self, instance: object) -> None:
        self.instance = instance


class ScopedServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredScopedServiceDefinition(ScopedServiceDefinition):

    def __init__(self, cls: type) -> None:
        self.cls = cls


class TransientServiceDefinition(ServiceDefinition, _ABC):
    pass


class RegisteredTransientServiceDefinition(TransientServiceDefinition):

    def __init__(self, cls: type) -> None:
        self.cls = cls
