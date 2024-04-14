from ..core import app_config

class Request(app_config.Request):

    _method: str
    _path: str

    def method(self) -> str:
        return self._method
    
    def set_method(self, method: str) -> None:
        self._method = method
    
    def path(self) -> str:
        return self._path
    
    def set_path(self, path: str) -> None:
        self._path = path
