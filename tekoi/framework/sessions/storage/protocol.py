from abc import abstractmethod as _abstractmethod
from typing import Protocol as _Protocol

class SessionStorageProtocol(_Protocol):
    
    @_abstractmethod
    def create_session(self, session_data) -> str:
        pass

    @_abstractmethod
    def get_session_data(self, session_id: str):
        pass

    @_abstractmethod
    def invalidate_session(self, session_id: str):
        pass
