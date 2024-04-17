from .route import Route
from .router import Router
from .handler import Handler

class Routing:

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def add_route(self, route: Route) -> None:
        self.routes.append(route)

    def router(self) -> Router:
        return Router(self.routes)
    
    def handler(self) -> Handler:
        return Handler()
