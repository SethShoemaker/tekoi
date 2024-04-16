import inspect

class ServiceContainer:

    def __init__(self) -> None:
        self._services: set[str] = set()
        self._instances: dict[type, object] = dict()

    def register_services(self, service_classes: list[type], insantiate_immediately: bool = False) -> None:
        for service_class in service_classes:
            self._services.add(service_class)
            if insantiate_immediately:
                self.resolve(service_class)

    def bind(self, service_class: str, instance: object):
        self._services.add(service_class)
        self._instances[service_class] = instance

    def has_instance(self, service_class: type) -> bool:
        return service_class in self._instances

    def resolve(self, service_class: str) -> object|None:
        if service_class not in self._services:
            return None
        if service_class not in self._instances:
            self.bind(service_class, construct_using_dependency_injection(service_class, [self], []))
        return self._instances[service_class]

def construct_using_dependency_injection(dependent_class: type, containers: list[ServiceContainer], transient_services: list[type]) -> object:
    signature = inspect.signature(dependent_class.__init__)
    parameters = {name: parameter.annotation for name, parameter in signature.parameters.items() if parameter.name != "self"}
    args = []
    for parameter_name, parameter_type in parameters.items():
        arg = None
        for container in containers:
            if arg is None:
                arg = container.resolve(parameter_type)
        if arg is None and parameter_type in transient_services:
            arg = construct_using_dependency_injection(parameter_type, containers, transient_services)
        if arg is None:
            raise ValueError("Cannot resolve argument " + parameter_name + " of class " + str(parameter_type))
        else:
            args.append(arg)
    return dependent_class(*args)
