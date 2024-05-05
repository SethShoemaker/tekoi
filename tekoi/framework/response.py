from tekoi.core import startup as _startup
import json as _json

class Response(_startup.Response):
    pass

def ok(body: bytes, content_type: str = "text/plain") -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.content_type = content_type
    res.status_code = 200
    return res

def ok_json(payload: dict|list) -> Response:
    return ok(
        body=_json.dumps(payload).encode(),
        content_type="application/json"
    )

def ok_created(body: bytes, content_type: str = "text/plain") -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.content_type = content_type
    res.status_code = 201
    return res

def ok_created_json(payload: dict|list) -> Response:
    return ok_created(
        body=_json.dumps(payload).encode(),
        content_type="application/json"
    )

def bad_request(body: bytes, content_type: str = "text/plain") -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.content_type = content_type
    res.status_code = 400
    return res

def bad_request_json(payload: dict|list) -> Response:
    return bad_request(
        body=_json.dumps(payload).encode(),
        content_type="application/json"
    )

def not_found(body: bytes, content_type: str = "text/plain") -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.content_type = content_type
    res.status_code = 404
    return res

def not_found_json(payload:dict) -> Response:
    return not_found(
        body=_json.dumps(payload).encode(),
        content_type="application/json"
    )

def internal_server_error(body: bytes, content_type: str = "text/plain") -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.content_type = content_type
    res.status_code = 500
    return res

def internal_server_error_json(payload: dict|list) -> Response:
    return internal_server_error(
        body=_json.dumps(payload).encode(),
        content_type="application/json"
    )
