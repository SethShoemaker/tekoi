import inspect

class SingletonContainer:
    
    def __init__(self) -> None:
        self._service_types: set[type] = set()
        self._service_instances: dict[type, object] = dict()
        self.bind_service_type(SingletonContainer, self)

    def register_service_type(self, service_type: list[type], insantiate_immediately: bool = False) -> None:
        self._service_types.add(service_type)
        if insantiate_immediately:
            self.resolve(service_type)

    def register_service_types(self, service_types:  list[type], insantiate_immediately: bool = False) -> None:
        for service_type in service_types:
            self.register_service_type(service_type, insantiate_immediately)

    def bind_service_type(self, service_type: type, instance: object) -> None:
        self._service_types.add(service_type)
        self._service_instances[service_type] = instance

    def has_service_instance(self, service_type: type) -> bool:
        return service_type in self._service_types
    
    def resolve_service(self, service_type: type) -> object|None:
        if service_type not in self._service_types:
            return None
        if service_type not in self._service_instances:
            self.bind_service_type(
                service_type, 
                construct_using_dependency_injection(
                    dependent_class=service_type, 
                    containers=[self]
                )
            )
        return self._service_instances[service_type]


class ScopedContainer:

    def __init__(self) -> None:
        self._singleton_container: SingletonContainer = None
        self._transient_service_types: set[type] = set()
        self._scoped_service_types: set[type] = set()
        self._scoped_service_instances: dict[type, object] = dict()
        self.bind_scoped_service_type(ScopedContainer, self)

    def set_singleton_container(self, singleton_container: SingletonContainer) -> None:
        self._singleton_container = singleton_container

    def register_transient_service_type(self, service_type: type) -> None:
        self._transient_service_types.add(service_type)

    def register_transient_service_types(self, service_types: list[type]) -> None:
        for service_type in service_types:
            self.register_transient_service_type(service_type)

    def register_scoped_service_type(self, service_type: list[type], insantiate_immediately: bool = False) -> None:
        self._scoped_service_types.add(service_type)
        if insantiate_immediately:
            self.resolve_scoped_service(service_type)

    def register_scoped_service_types(self, service_types:  list[type], insantiate_immediately: bool = False) -> None:
        for service_type in service_types:
            self.register_scoped_service_type(service_type, insantiate_immediately)

    def bind_scoped_service_type(self, service_type: type, instance: object) -> None:
        self._scoped_service_types.add(service_type)
        self._scoped_service_instances[service_type] = instance

    def has_scoped_service_instance(self, service_type: type) -> bool:
        return service_type in self._scoped_service_instances
    
    def resolve_scoped_service(self, scoped_service_type: type) -> object|None:
        if scoped_service_type not in self._scoped_service_types:
            return None
        if scoped_service_type not in self._scoped_service_instances:
            self.bind_scoped_service_type(
                scoped_service_type, 
                construct_using_dependency_injection(
                    dependent_class=scoped_service_type,
                    singleton_container=self._singleton_container,
                    scoped_container=self
                )
            )
        return self._scoped_service_instances[scoped_service_type]
    
    def resolve_transient_service(self, transient_service_type: type) -> object|None:
        if transient_service_type not in self._transient_service_types:
            return None
        return construct_using_dependency_injection(
            dependent_class=transient_service_type,
            singleton_container=self._singleton_container,
            scoped_container=self
        )
    
    def resolve_service(self, service_type) -> object|None:
        scoped_service_instance = self.resolve_scoped_service(service_type)
        if scoped_service_instance is not None:
            return scoped_service_instance
        transient_service_instance = self.resolve_transient_service(service_type)
        if transient_service_instance is not None:
            return transient_service_instance
        return None


def construct_using_dependency_injection(dependent_class: type, 
                                         singleton_container: SingletonContainer,
                                         scoped_container: ScopedContainer,
                                         extra_services: dict[type, object] = {}
                                         ) -> object:
    signature = inspect.signature(dependent_class.__init__)
    parameters = {name: parameter.annotation for name, parameter in signature.parameters.items() if parameter.name != "self"}
    args = []
    for parameter_name, parameter_type in parameters.items():
        arg = None
        if arg is None and singleton_container is not None:
            arg = singleton_container.resolve_service(parameter_type)
        if arg is None and scoped_container is not None:
            arg = scoped_container.resolve_service(parameter_type)
        if arg is None and parameter_type in extra_services:
            arg = extra_services[parameter_type]
        if arg is None:
            raise ValueError("Cannot resolve argument " + parameter_name + " of class " + str(parameter_type))
        else:
            args.append(arg)
    return dependent_class(*args)
