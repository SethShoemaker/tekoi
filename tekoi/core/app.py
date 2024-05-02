import webob as _webob
from . import services as _services
from . import startup as _startup

class App:

    def __init__(self, 
                 request_class: type[_startup.Request],
                 response_class: type[_startup.Response],
                 service_definitions: list[_startup.ServiceDefinition],
                 pipeline_member_definitions: list[_startup.PipelineMemberDefinition],
                 background_service_definitions: list[_startup.BackgroundServiceDefinition]
                 ):
        self.request_class = request_class
        self.response_class = response_class

        self.pipeline_member_definitions = pipeline_member_definitions
        self.singleton_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, _startup.SingletonPipelineMemberDefinition)]
        self.scoped_pipeline_member_definitions = [definition for definition in self.pipeline_member_definitions if isinstance(definition, _startup.ScopedPipelineMemberDefinition)]
        
        self.service_definitions = service_definitions
        self.singleton_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _startup.SingletonServiceDefinition)]
        self.scoped_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _startup.ScopedServiceDefinition)]
        self.transient_service_definitions = [definition for definition in self.service_definitions if isinstance(definition, _startup.TransientServiceDefinition)]

        self.singleton_container = _services.SingletonContainer()
        self.bootstrap_singleton_services()
        self.bootstrap_singleton_pipeline_members()

        self.background_service_definitions = background_service_definitions
        self.bootstrap_background_services()
        self.start_background_services()

    def bootstrap_singleton_services(self) -> None:
        for definition in self.singleton_service_definitions:
            if isinstance(definition, _startup.RegisteredSingletonServiceDefinition):
                self.singleton_container.register_singleton_service(definition.interface, definition.implementation)
                continue
            if isinstance(definition, _startup.BindedSingletonServiceDefinition):
                self.singleton_container.bind_singleton_service(definition.interface, definition.instance)
                continue
            raise NotImplementedError()

    def bootstrap_singleton_pipeline_members(self) -> None:
        for definition in self.singleton_pipeline_member_definitions:
            if isinstance(definition, _startup.BindedSingletonPipelineMemberDefinition):
                self.singleton_container.bind_singleton_service(type(definition.instance), definition.instance)
                continue
            if isinstance(definition, _startup.RegisteredSingletonPipelineMemberDefinition):
                self.singleton_container.register_singleton_service(definition.cls, definition.cls, instantiate_immediately=True)
                continue
            raise NotImplementedError()
        
    def bootstrap_background_services(self) -> None:
        for definition in self.background_service_definitions:
            self.singleton_container.register_singleton_service(definition.cls, definition.cls, instantiate_immediately=True)

    def start_background_services(self) -> None:
        for definition in self.background_service_definitions:
            instance = self.singleton_container.resolve_singleton_service(definition.cls)
            if not isinstance(instance, _startup.BackgroundService):
                raise TypeError("BackgroundService must inherit from BackgroundService")
            instance.start()

    def __call__(self, environ, start_response):
        webob_request = _webob.Request(environ)
        app_request = self.request_class()
        app_request.method = webob_request.method
        app_request.path = webob_request.path
        app_request.cookies = _startup.RequestCookieCollection([_startup.RequestCookie(name, value) for name, value in webob_request.cookies.items()])
        app_request.body = webob_request.body

        app_response = RequestHandler(self, app_request)()
        webob_response = _webob.Response()
        webob_response.body = app_response.body
        webob_response.status = app_response.status_code
        webob_response.content_type = app_response.content_type
        [webob_response.set_cookie(name, value) for name, value in app_response.cookies.items.items()]

        return webob_response(environ, start_response)


class RequestHandler:

    def __init__(self, app: App, request: _startup.Request) -> None:
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
        self.scoped_container._singleton_container = self.singleton_container
        self.register_transient_service_types()
        self.register_scoped_service_types()
        self.register_and_instantiate_scoped_pipleline_members()

    def register_scoped_service_types(self) -> None:
        for definition in self.scoped_service_definitions:
            if isinstance(definition, _startup.RegisteredScopedServiceDefinition):
                self.scoped_container.register_scoped_service(definition.interface, definition.implementation)
                continue
            raise NotImplementedError()
        
    def register_transient_service_types(self) -> None:
        for definition in self.transient_service_definitions:
            if isinstance(definition, _startup.RegisteredTransientServiceDefinition):
                self.scoped_container.register_transient_service(definition.interface, definition.implementation)
                continue
            raise NotImplementedError()
        
    def register_and_instantiate_scoped_pipleline_members(self) -> None:
        for definition in self.scoped_pipeline_member_definitions:
            if isinstance(definition, _startup.RegisteredScopedPipelineMemberDefinition):
                self.scoped_container.register_scoped_service(definition.cls, definition.cls, instantiate_immediately=True)
                continue
            raise NotImplementedError()

    def __call__(self) -> _startup.Response:

        next = lambda request: self.response_class()

        for definition in reversed(self.pipeline_member_definitions):
            instance = self.get_pipeline_member_instance(definition)
            next = (lambda member_instance, next: lambda request: member_instance(request, next))(instance, next)
        
        return next(self.request)
    
    def get_pipeline_member_instance(self, definition: _startup.PipelineMemberDefinition) -> _startup.PipelineMemberProtocol:
        if isinstance(definition, _startup.SingletonPipelineMemberDefinition):
            if isinstance(definition, _startup.RegisteredSingletonPipelineMemberDefinition):
                return self.singleton_container.resolve_singleton_service(definition.cls) # type: ignore
            if isinstance(definition, _startup.BindedSingletonPipelineMemberDefinition):
                return definition.instance
            raise NotImplementedError()
        if isinstance(definition, _startup.ScopedPipelineMemberDefinition):
            if isinstance(definition, _startup.RegisteredScopedPipelineMemberDefinition):
                return self.scoped_container.resolve_scoped_service(definition.cls) # type: ignore
            raise NotImplementedError()
        raise NotImplementedError()
