class Response:

    status_code: int = 200
    status_message: str = "OK"
    content_type: str = "text/plain"
    content_length : int = len(b"Hello World")
    body: bytes = b"Hello World"
