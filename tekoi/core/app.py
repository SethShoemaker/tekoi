from tekoi.components import dependency_injection
from . import app_config

class RequestHandler:

    def __init__(self, 
                 request: app_config.Request,
                 response_class: type[app_config.Response],
                 pipeline_definition: app_config.PipelineDefinitionProtocol,
                 singleton_container: dependency_injection.ServiceContainer,
                 scoped_service_classes: list[type],
                 transient_service_classes: list[type]
                 ) -> None:
        self.request: app_config.Request = request
        self.response_class: type[app_config.Response] = response_class
        self.pipeline_definition: app_config.PipelineDefinitionProtocol = pipeline_definition
        self.singleton_container: dependency_injection.ServiceContainer = singleton_container
        self.scoped_service_classes: list[type] = scoped_service_classes
        self.transient_service_classes = transient_service_classes

    def __call__(self) -> app_config.Response:

        scoped_container = dependency_injection.ServiceContainer()
        scoped_container.register_services(self.scoped_service_classes)

        next = lambda request: self.response_class()
        
        for definition in self.pipeline_definition.get_members().__reversed__():
            pipeline_member_lifetime = definition.lifetime()
            pipeline_member_class = definition.class_name()

            if pipeline_member_lifetime == "scoped":
                member_instance = dependency_injection.construct_using_dependency_injection(pipeline_member_class, containers=[self.singleton_container, scoped_container], transient_services=self.transient_service_classes)
            else:
                member_instance = self.singleton_container.resolve(pipeline_member_class)

            if member_instance is None:
                raise Exception(f'couldn\'t create {pipeline_member_class}')
            
            next = (lambda member_instance, next: lambda request: member_instance(request, next))(member_instance, next)

        return next(self.request)


class App:

    def __init__(self, 
                 request_class: type[app_config.Request],
                 response_class: type[app_config.Response],
                 container_definition: app_config.ContainerDefinitionProtocol,
                 pipeline_definition: app_config.PipelineDefinitionProtocol
                 ) -> None:
        self.request_class = request_class
        self.response_class = response_class

        self.pipeline_definition = pipeline_definition

        self.singleton_container = dependency_injection.ServiceContainer()
        self.singleton_container.register_services([definition.class_name() for definition in container_definition.get_singleton_service_definitions()])
        self.singleton_container.register_services([definition.class_name() for definition in pipeline_definition.get_members() if definition.lifetime() == "singleton"], insantiate_immediately=True)

        self.scoped_service_classes = [definition.class_name() for definition in container_definition.get_scoped_service_definitions()]
        self.scoped_pipeline_member_classes = [definition.class_name() for definition in pipeline_definition.get_members() if definition.lifetime() == "scoped"]

        self.transient_service_classes = [definition.class_name() for definition in container_definition.get_transient_service_definitions()]

    def __call__(self, environ, start_response):
        request = self.request_class()
        request.set_method(environ.get('REQUEST_METHOD'))
        request.set_path(environ.get('PATH_INFO'))

        handler = RequestHandler(
            request=request,
            response_class=self.response_class,
            pipeline_definition=self.pipeline_definition,
            singleton_container=self.singleton_container,
            scoped_service_classes=self.scoped_service_classes,
            transient_service_classes=self.transient_service_classes
        )

        response = handler()

        start_response(f"{response.status_code()} {response.status_message()}", [
            ("Content-Type", response.content_type()),
            ("Content-Length", str(len(response.body())))
        ])
        return [response.body()]
