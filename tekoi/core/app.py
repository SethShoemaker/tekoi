import webob as _webob
from . import services as _services
from . import app_config as _app_config

class App:

    def __init__(self, 
                 request_class: type[_app_config.Request],
                 response_class: type[_app_config.Response],
                 service_definitions: list[_app_config.ServiceDefinition],
                 pipeline_member_definitions: list[_app_config.PipelineMemberDefinition],
                 background_service_definitions: list[_app_config.BackgroundServiceDefinition]
                 ):
        self.request_class = request_class
        self.response_class = response_class

        self.pipeline_member_definitions = pipeline_member_definitions
        self.singleton_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, _app_config.SingletonPipelineMemberDefinition)]
        self.scoped_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, _app_config.ScopedPipelineMemberDefinition)]
        
        self.service_definitions = service_definitions
        self.singleton_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _app_config.SingletonServiceDefinition)]
        self.scoped_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _app_config.ScopedServiceDefinition)]
        self.transient_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _app_config.TransientServiceDefinition)]

        self.singleton_container = _services.SingletonContainer()
        self.register_singleton_service_types()
        self.register_and_instantiate_singleton_pipeline_members()

        self.background_service_definitions = background_service_definitions
        self.register_and_instantiate_background_services()
        self.start_background_services()

    def register_singleton_service_types(self) -> None:
        for definition in self.singleton_service_definitions:
            if isinstance(definition, _app_config.BindedSingletonServiceDefinition):
                self.singleton_container.bind_service_type(type(definition.instance), definition.instance)
                continue
            if isinstance(definition, _app_config.RegisteredSingletonServiceDefinition):
                self.singleton_container.register_service_type(definition.cls)
                continue
            raise NotImplementedError()

    def register_and_instantiate_singleton_pipeline_members(self) -> None:
        for definition in self.singleton_pipeline_member_definitions:
            if isinstance(definition, _app_config.BindedSingletonPipelineMemberDefinition):
                self.singleton_container.bind_service_type(type(definition.instance), definition.instance)
                continue
            if isinstance(definition, _app_config.RegisteredSingletonPipelineMemberDefinition):
                self.singleton_container.register_service_type(definition.cls, insantiate_immediately=True)
                continue
            raise NotImplementedError()
        
    def register_and_instantiate_background_services(self) -> None:
        for definition in self.background_service_definitions:
            self.singleton_container.register_service_type(definition.cls, insantiate_immediately=True)

    def start_background_services(self) -> None:
        for definition in self.background_service_definitions:
            instance = self.singleton_container.resolve_service(definition.cls)
            if not isinstance(instance, _app_config.BackgroundService):
                raise TypeError("BackgroundService must inherit from BackgroundService")
            instance.start()

    def __call__(self, environ, start_response):
        webob_request = _webob.Request(environ)
        app_request = self.request_class()
        app_request.method = webob_request.method
        app_request.path = webob_request.path
        app_request.cookies = _app_config.RequestCookieCollection([_app_config.RequestCookie(name, value) for name, value in webob_request.cookies.items()])

        app_response = RequestHandler(self, app_request)()
        webob_response = _webob.Response()
        webob_response.body = app_response.body
        webob_response.status = app_response.status_code
        webob_response.content_type = app_response.content_type
        [webob_response.set_cookie(name, value) for name, value in app_response.cookies.items.items()]

        return webob_response(environ, start_response)


class RequestHandler:

    def __init__(self, app: App, request: _app_config.Request) -> None:
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
        
        self.scoped_container = _services.ScopedContainer()
        self.scoped_container.set_singleton_container(self.singleton_container)
        self.register_transient_service_types()
        self.register_scoped_service_types()
        self.register_and_instantiate_scoped_pipleline_members()

    def register_scoped_service_types(self) -> None:
        for definition in self.scoped_service_definitions:
            if isinstance(definition, _app_config.RegisteredScopedServiceDefinition):
                self.scoped_container.register_scoped_service_type(definition.cls)
                continue
            raise NotImplementedError()
        
    def register_transient_service_types(self) -> None:
        for definition in self.transient_service_definitions:
            if isinstance(definition, _app_config.RegisteredTransientServiceDefinition):
                self.scoped_container.register_transient_service_type(definition.cls)
                continue
            raise NotImplementedError()
        
    def register_and_instantiate_scoped_pipleline_members(self) -> None:
        for definition in self.scoped_pipeline_member_definitions:
            if isinstance(definition, _app_config.RegisteredScopedPipelineMemberDefinition):
                self.scoped_container.register_scoped_service_type(definition.cls, insantiate_immediately=True)
                continue
            raise NotImplementedError()

    def __call__(self) -> _app_config.Response:

        next = lambda request: self.response_class()

        for definition in reversed(self.pipeline_member_definitions):
            instance = self.get_pipeline_member_instance(definition)
            next = (lambda member_instance, next: lambda request: member_instance(request, next))(instance, next)
        
        return next(self.request)
    
    def get_pipeline_member_instance(self, definition: _app_config.PipelineMemberDefinition) -> _app_config.PipelineMemberProtocol:
        if isinstance(definition, _app_config.SingletonPipelineMemberDefinition):
            if isinstance(definition, _app_config.RegisteredSingletonPipelineMemberDefinition):
                return self.singleton_container.resolve_service(definition.cls) # type: ignore
            if isinstance(definition, _app_config.BindedSingletonPipelineMemberDefinition):
                return definition.instance
            raise NotImplementedError()
        if isinstance(definition, _app_config.ScopedPipelineMemberDefinition):
            if isinstance(definition, _app_config.RegisteredScopedPipelineMemberDefinition):
                return self.scoped_container.resolve_scoped_service(definition.cls) # type: ignore
            raise NotImplementedError()
        raise NotImplementedError()
