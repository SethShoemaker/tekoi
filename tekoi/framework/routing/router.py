from .route import Route as _Route
from tekoi.framework import (Request as _Request, 
                             Response as _Response, 
                             PipelineMember as _PipelineMember)
import typing

class Router(_PipelineMember):

    def __init__(
            self,
            routes: list[_Route]
        ):
        self.routes = routes

    def __call__(self, request: _Request, next: typing.Callable[[_Request], _Response]) -> _Response:

        for route in self.routes:

            match_result = self.match_route(
                request_method=request.method, # type: ignore
                request_path=request.path, # type: ignore
                route_method=route.method,
                route_path=route.path
            )

            if match_result == False:
                continue

            request.routing_target = route.cls
            request.routing_path_params = match_result # type: ignore
            break

        return next(request)
    
    def match_route(self, request_method: str, request_path: str, route_method: str, route_path: str) -> dict[str, str]|bool:

        if request_method != route_method:
            return  False
        
        request_path_segments = [segment for segment in request_path.split('/') if segment]
        route_path_segments = [segment for segment in route_path.split('/') if segment]

        path_params: dict[str, str] = {}

        for i in range(len(request_path_segments)):

            if not 0 <= i < len(request_path_segments):
                return False
            
            if not 0 <= i < len(route_path_segments):
                return False

            request_path_segment = request_path_segments[i]
            route_path_segment = route_path_segments[i]

            route_path_segment_is_variable = route_path_segment[0] == ":"
            route_path_segment_is_partial_wildcard = route_path_segment == "*"
            route_path_segment_is_complete_wildcard = route_path_segment == "**"
            path_segments_match = request_path_segment == route_path_segment

            if ((route_path_segment_is_variable == False) and 
                (path_segments_match == False) and 
                (route_path_segment_is_partial_wildcard == False) and 
                (route_path_segment_is_complete_wildcard == False)):
                return False
            
            if (route_path_segment_is_variable == False) and path_segments_match:
                continue

            if route_path_segment_is_partial_wildcard:
                continue

            if route_path_segment_is_complete_wildcard:
                return path_params

            route_path_segment_variable_name = route_path_segment[1:]
            route_path_segment_variable_value = request_path_segment
            path_params[route_path_segment_variable_name] = route_path_segment_variable_value

        return path_params
