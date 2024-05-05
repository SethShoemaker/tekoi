from .storage import SessionStorageProtocol as _SessionStorageProtocol
from ..builder import AppBuilder as _AppBuilder

class SessionsDefinition:

    def __init__(self, builder: _AppBuilder) -> None:
        self._builder = builder
        self.storage: _SessionStorageProtocol|None = None

    def set_storage(self, storage: _SessionStorageProtocol) -> None:
        self.storage = storage
        self._builder.services.bind_singleton(_SessionStorageProtocol, storage)
