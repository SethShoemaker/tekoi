class Response:

    status_code: int = 200
    status_message: str = "OK"
    content_type: str = "text/plain"
    content_length : int = len(b"Hello World")
    body: str = b"Hello World"
