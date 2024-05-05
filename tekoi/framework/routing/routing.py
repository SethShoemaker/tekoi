from .route import Route as _Route
from ..builder import AppBuilder as _AppBuilder

class RoutingDefinition:

    def __init__(self, builder: _AppBuilder) -> None:
        self._builder = builder
        self.routes: list[_Route] = []

    def add_route(self, route: _Route) -> None:
        self.routes.append(route)
        self._builder.services.register_scoped(route.cls, route.cls)
