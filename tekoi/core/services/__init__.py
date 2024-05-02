import inspect as _inspect

class SingletonContainer:
    
    def __init__(self) -> None:
        self._singleton_implementations: dict[type, type] = dict()
        self._singleton_instances: dict[type, object] = dict()
        self.register_singleton_service(SingletonContainer, SingletonContainer)
        self.bind_singleton_service(SingletonContainer, self)

    def register_singleton_service(self, interface: type, implementation: type, instantiate_immediately: bool = False) -> None:
        self._singleton_implementations[interface] = implementation
        self._singleton_instances[interface] = None
        if instantiate_immediately:
            self.resolve_singleton_service(interface)

    def bind_singleton_service(self, interface: type, instance: object) -> None:
        self._singleton_implementations[interface] = type(instance)
        self._singleton_instances[interface] = instance
    
    def resolve_singleton_service(self, interface: type) -> object|None:
        if interface not in self._singleton_implementations:
            return None
        if self._singleton_instances[interface] is None:
            self.bind_singleton_service(
                interface, 
                construct_using_dependency_injection(
                    dependent_class=self._singleton_implementations[interface], 
                    singleton_container=self,
                    scoped_container=None
                )
            )
        return self._singleton_instances[interface]


class ScopedContainer:

    def __init__(self) -> None:
        self._singleton_container: SingletonContainer
        self._transient_implementations: dict[type, type] = dict()
        self._scoped_implementations: dict[type, type] = dict()
        self._scoped_instances: dict[type, object] = dict()
        self.register_scoped_service(ScopedContainer, ScopedContainer)
        self.bind_scoped_service(ScopedContainer, self)

    def register_transient_service(self, interface: type, implementation: type) -> None:
        self._transient_implementations[interface] = implementation

    def resolve_transient_service(self, interface: type) -> object|None:
        if interface not in self._transient_implementations:
            return None
        return construct_using_dependency_injection(
            dependent_class=self._transient_implementations[interface],  
            singleton_container=self._singleton_container,
            scoped_container=self
        )

    def register_scoped_service(self, interface: type, implementation: type, instantiate_immediately: bool = False) -> None:
        self._scoped_implementations[interface] = implementation
        self._scoped_instances[interface] = None
        if instantiate_immediately:
            self.resolve_scoped_service(interface)

    def bind_scoped_service(self, interface: type, instance: object) -> None:
        self._scoped_implementations[interface] = type(instance)
        self._scoped_instances[interface] = instance

    def resolve_scoped_service(self, interface: type) -> object|None:
        if interface not in self._scoped_implementations:
            return None
        if self._scoped_instances[interface] is None:
            self._scoped_instances[interface] = construct_using_dependency_injection(
                dependent_class=self._scoped_implementations[interface],
                singleton_container=self._singleton_container,
                scoped_container=self
            )
        return self._scoped_instances[interface]


def construct_using_dependency_injection(
        dependent_class: type, 
        singleton_container: SingletonContainer|None = None,
        scoped_container: ScopedContainer|None = None,
        extra_services: dict[type, object] = {}
    ) -> object:
    signature = _inspect.signature(dependent_class.__init__) # type: ignore
    parameters = {name: parameter.annotation for name, parameter in signature.parameters.items() if parameter.name != "self"}
    args = []
    for parameter_name, parameter_type in parameters.items():
        arg = None
        if arg is None and singleton_container is not None:
            arg = singleton_container.resolve_singleton_service(parameter_type)
        if arg is None and scoped_container is not None:
            arg = scoped_container.resolve_scoped_service(parameter_type)
        if arg is None and scoped_container is not None:
            arg = scoped_container.resolve_transient_service(parameter_type)
        if arg is None and parameter_type in extra_services:
            arg = extra_services[parameter_type]
        if arg is None:
            raise ValueError(f"Cannot construct {dependent_class}, error resolving argument " + parameter_name + " of type " + str(parameter_type))
        else:
            args.append(arg)
    return dependent_class(*args)
