from tekoi.framework.routing import Route
from tekoi.framework import Request, Response, PipelineMember

class Router(PipelineMember):

    def __init__(
            self,
            routes: list[Route]
        ):
        self.routes = routes

    def __call__(self, request: Request, next: callable) -> Response:

        for route in self.routes:

            path_params = self.get_path_params(request, route)

            if path_params == False:
                continue

            request.routing_target = route
            request.path_params = path_params
            break

        return next(request)

    def get_path_params(self, request: Request, route: Route) -> dict[str, str]|bool:

        if request.method != route.method:
            return  False
        
        request_path_segments: list[str] = [segment for segment in request.path.split('/') if segment]
        route_path_segments: list[str] = [segment for segment in route.path.split('/') if segment]

        if len(request_path_segments) != len(route_path_segments):
            return False

        path_params: dict[str, str] = []

        for i in range(len(request_path_segments)):
            request_path_segment = request_path_segments[i]
            route_path_segment = route_path_segments[i]

            route_path_segment_is_variable = route_path_segment[0] == ":"
            path_segments_match = request_path_segment == route_path_segment

            if (route_path_segment_is_variable == False) and (path_segments_match == False):
                return False
            
            if (route_path_segment_is_variable == False) and (path_segments_match):
                continue

            route_path_segment_variable_name = route_path_segment[1:]
            route_path_segment_variable_value = request_path_segment
            path_params[route_path_segment_variable_name] = route_path_segment_variable_value

        return path_params
