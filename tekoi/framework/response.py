from tekoi.core import startup as _startup
import json as _json

class Response(_startup.Response):
    pass

def ok(body: bytes) -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.status_code = 200
    return res

def ok_json(payload: dict|list) -> Response:
    return ok(body=_json.dumps(payload).encode())

def ok_created(body: bytes) -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.status_code = 201
    return res

def ok_created_json(payload: dict|list) -> Response:
    return ok_created(body=_json.dumps(payload).encode())

def bad_request(body: bytes) -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.status_code = 400
    return res

def bad_request_json(payload: dict|list) -> Response:
    return bad_request(_json.dumps(payload).encode())

def not_found(body: bytes) -> Response:
    res = Response()
    res.body = body
    res.content_length = len(body)
    res.status_code = 404
    return res

def not_found_json(payload:dict) -> Response:
    return not_found(_json.dumps(payload).encode())
