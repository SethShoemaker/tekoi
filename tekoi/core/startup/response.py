class ResponseCookieCollection:

    def __init__(self) -> None:
        self.items: dict[str, str] = dict()

    def set(self, name: str, value: str) -> None:
        self.items[name] = value

class Response:

    status_code: int = 200
    content_type: str = "text/plain"
    content_length : int = len(b"Hello World")
    body: bytes = b"Hello World"
    cookies: ResponseCookieCollection = ResponseCookieCollection()
