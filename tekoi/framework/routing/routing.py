from tekoi.framework.builder import AppBuilder
from .route import Route
from .router import Router
from .handler import Handler

class Routing:

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def add_route(self, route: Route) -> None:
        self.routes.append(route)

    def router(self):
        return Router(self.routes)
    
    def handler(self):
        return Handler
    
    def register_route_clss(self, builder: AppBuilder) -> None:
        for route in self.routes:
            builder.services.register_scoped(route.cls)
