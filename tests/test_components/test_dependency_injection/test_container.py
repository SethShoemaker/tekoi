import unittest
from tekoi.components.dependency_injection.container import ServiceContainer, construct_using_dependency_injection

class Service1:
    def __init__(self) -> None:
        pass

class Service2:
    def __init__(self) -> None:
        pass

class Service3:
    def __init__(self, service_1: Service1, service_2: Service2) -> None:
        self.service_1 = service_1
        self.service_2 = service_2

class Service4:
    def __init__(self, service_3: Service3) -> None:
        self.service_3 = service_3

class test_service_container_test(unittest.TestCase):

    def test_resolve_constructs_services_with_parameterless_constructors(self):
        container = ServiceContainer()
        container.register_services([Service1])

        service_1 = container.resolve(Service1)

        self.assertIsNotNone(service_1)
        self.assertIsInstance(service_1, Service1)

    def test_resolve_with_immediate_instantiation_immediately_instantiates_services(self):
        container = ServiceContainer()
        container.register_services([Service1, Service2, Service3], insantiate_immediately=True)

        self.assertTrue(container.has_instance(Service1))
        self.assertTrue(container.has_instance(Service2))
        self.assertTrue(container.has_instance(Service3))

    def test_resolve_returns_none_when_service_is_not_registered(self):
        container = ServiceContainer()
        container.register_services([Service1])

        service2 = container.resolve(Service2)
        self.assertIsNone(service2)

    def test_resolve_constructs_service_with_injection_if_it_has_constructor_parameters(self):
        container = ServiceContainer()
        container.register_services([Service1, Service2, Service3])

        service3 = container.resolve(Service3)

        self.assertIsNotNone(service3)
        self.assertIsInstance(service3, Service3)

class construct_using_dependency_injection_test(unittest.TestCase):

    def test_constructs_service_with_constructor_parameters(self):
        container = ServiceContainer()
        container.register_services([Service1, Service2])

        service3 = construct_using_dependency_injection(Service3, [container], [])

        self.assertIsNotNone(service3)
        self.assertIsInstance(service3, Service3)
        self.assertIsInstance(service3.service_1, Service1)
        self.assertIsInstance(service3.service_2, Service2)

    def test_constructs_service_with_no_constructor_params(self):
        container = ServiceContainer()
        container.register_services([Service1])

        service2 = construct_using_dependency_injection(Service2, [container], [])

        self.assertIsNotNone(service2)
        self.assertIsInstance(service2, Service2)

    def test_constructs_service_with_dependencies_from_multiple_service_containers(self):
        container_1 = ServiceContainer()
        container_1.register_services([Service1])

        container_2 = ServiceContainer()
        container_2.register_services([Service2])

        service3 = construct_using_dependency_injection(Service3, [container_1, container_2], [])

        self.assertIsNotNone(service3)
        self.assertIsInstance(service3, Service3)
        self.assertIsInstance(service3.service_1, Service1)
        self.assertIsInstance(service3.service_2, Service2)

    def test_constructs_service_with_dependencies_from_multiple_service_containers_and_transient_services(self):
        container = ServiceContainer()
        container.register_services([Service1, Service2])

        service4 = construct_using_dependency_injection(Service4, [container], [Service3])

        self.assertIsNotNone(service4)
        self.assertIsInstance(service4, Service4)
        self.assertIsInstance(service4.service_3, Service3)
