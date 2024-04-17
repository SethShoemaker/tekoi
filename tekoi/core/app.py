from tekoi.components import dependency_injection
from . import app_config

class App:

    def __init__(self, 
                 request_class: type[app_config.Request],
                 response_class: type[app_config.Response],
                 service_definitions: list[app_config.ServiceDefinition],
                 pipeline_member_definitions: list[app_config.PipelineMemberDefinition]
                 ):
        self.request_class = request_class
        self.response_class = response_class

        self.pipeline_member_definitions = pipeline_member_definitions
        self.singleton_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, app_config.SingletonPipelineMemberDefinition)]
        self.scoped_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, app_config.ScopedPipelineMemberDefinition)]
        
        self.service_definitions = service_definitions
        self.singleton_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, app_config.SingletonServiceDefinition)]
        self.scoped_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, app_config.ScopedServiceDefinition)]
        self.transient_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, app_config.TransientServiceDefinition)]

        self.singleton_container = dependency_injection.ServiceContainer()
        self.register_singleton_services()
        self.register_singleton_pipeline_members()

    def register_singleton_services(self) -> None:
        for definition in self.singleton_service_definitions:
            if isinstance(definition, app_config.BindedSingletonServiceDefinition):
                self.singleton_container.bind(type(definition.instance), definition.instance)
                continue
            if isinstance(definition, app_config.RegisteredSingletonServiceDefinition):
                self.singleton_container.register_services([definition.cls])
                continue
            raise NotImplementedError()

    def register_singleton_pipeline_members(self) -> None:
        for definition in self.singleton_pipeline_member_definitions:
            if isinstance(definition, app_config.BindedSingletonPipelineMemberDefinition):
                self.singleton_container.bind(type(definition.instance), definition.instance)
                continue
            if isinstance(definition, app_config.RegisteredSingletonPipelineMemberDefinition):
                self.singleton_container.register_services([definition.cls], insantiate_immediately=True)
                continue
            raise NotImplementedError()

    def __call__(self, environ, start_response):
        request = self.request_class()
        request.method = (environ.get('REQUEST_METHOD'))
        request.path = (environ.get('PATH_INFO'))

        response = RequestHandler(self, request)()

        start_response(f"{response.status_code} {response.status_message}", [
            ("Content-Type", response.content_type),
            ("Content-Length", str(len(response.body)))
        ])
        return [response.body]


class RequestHandler:

    def __init__(self, app: App, request: app_config.Request) -> None:
        self.request = request
        self.response_class = app.response_class

        self.pipeline_member_definitions = app.pipeline_member_definitions
        self.singleton_pipeline_member_definitions = app.singleton_pipeline_member_definitions
        self.scoped_pipeline_member_definitions = app.scoped_pipeline_member_definitions

        self.service_definitions = app.service_definitions
        self.singleton_service_definitions = app.singleton_service_definitions
        self.scoped_service_definitions = app.scoped_service_definitions
        self.transient_service_definitions = app.transient_service_definitions

        self.singleton_container = app.singleton_container
        
        self.scoped_container = dependency_injection.ServiceContainer()
        self.register_scoped_services()
        self.register_scoped_pipeline_members()

    def register_scoped_services(self) -> None:
        for definition in self.scoped_service_definitions:
            if isinstance(definition, app_config.RegisteredScopedServiceDefinition):
                self.scoped_container.register_services([definition.cls])
                continue
            raise NotImplementedError()
        
    def register_scoped_pipeline_members(self) -> None:
        for definition in self.scoped_pipeline_member_definitions:
            if isinstance(definition, app_config.RegisteredScopedPipelineMemberDefinition):
                self.scoped_container.register_services([definition.cls])
                continue
            raise NotImplementedError()

    def __call__(self) -> app_config.Response:

        next = lambda request: self.response_class()

        for definition in reversed(self.pipeline_member_definitions):
            instance = self.get_pipeline_member_instance(definition)
            next = (lambda member_instance, next: lambda request: member_instance(request, next))(instance, next)
        
        return next(self.request)
    
    def get_pipeline_member_instance(self, definition: app_config.PipelineMemberDefinition) -> app_config.PipelineMemberProtocol:
        if isinstance(definition, app_config.SingletonPipelineMemberDefinition):
            if isinstance(definition, app_config.RegisteredSingletonPipelineMemberDefinition):
                return self.singleton_container.resolve(definition.cls)
            if isinstance(definition, app_config.BindedSingletonPipelineMemberDefinition):
                return definition.instance
            raise NotImplementedError()
        if isinstance(definition, app_config.ScopedPipelineMemberDefinition):
            if isinstance(definition, app_config.RegisteredScopedPipelineMemberDefinition):
                return dependency_injection.construct_using_dependency_injection(
                    definition.cls, 
                    containers=[self.singleton_container, self.scoped_container], 
                    transient_services=[definition.cls for definition in self.transient_service_definitions if isinstance(definition, app_config.RegisteredTransientServiceDefinition)]
                )
            raise NotImplementedError()
        raise NotImplementedError()
