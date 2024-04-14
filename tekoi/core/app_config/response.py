class Response:

    def status_code(self) -> int:
        pass

    def set_status_code(self, status_code: int) -> None:
        pass

    def status_message(self) -> str:
        pass

    def set_status_message(self, status_message: str) -> None:
        pass

    def content_type(self) -> str:
        pass

    def set_content_type(self, content_type: str) -> None:
        pass

    def content_length(self) -> str:
        pass

    def set_content_length(self, content_length: int) -> None:
        pass

    def body(self) -> str:
        pass

    def set_body(self, body: str) -> None:
        pass
