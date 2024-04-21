from .storage import (SessionStorageProtocol as _SessionStorageProtocol)
from .handler import (Handler as _Handler)

class Sessions:

    def __init__(self) -> None:
        self.storage: _SessionStorageProtocol|None = None

    def set_storage(self, storage: _SessionStorageProtocol) -> None:
        self.storage = storage

    def handler(self):
        return _Handler(self.storage)
