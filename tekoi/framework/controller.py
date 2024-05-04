from .pipeline import PipelineMember as _PipelineMember
from .request import Request as _Request
import json as _json

class Controller(_PipelineMember):
    
    def get_json_request_body(self, request: _Request) -> bool:
        if request.body is None:
            return False
        try:
            body = _json.loads(request.body)
            return body
        except _json.JSONDecodeError:
            return False
