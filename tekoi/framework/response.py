from ..core import app_config

class Response(app_config.Response):

    _status_code: int = 200
    _status_message: str = "OK"
    _content_type: str = "text/plain"
    _content_length : int = len(b"Hello World")
    _body: str = b"Hello World"

    def status_code(self) -> int:
        return self._status_code
    
    def set_status_code(self, status_code: int) -> None:
        self._status_code = status_code

    def status_message(self) -> str:
        return self._status_message
    
    def set_status_message(self, status_message: str) -> None:
        self._status_message = status_message

    def content_type(self) -> str:
        return self._content_type
    
    def set_content_type(self, content_type: str) -> None:
        self._content_type = content_type

    def content_length(self) -> str:
        return self._content_length
    
    def set_content_length(self, content_length: int) -> None:
        self._content_length = content_length

    def body(self) -> str:
        return self._body
    
    def set_body(self, body: str) -> None:
        self._body = body
