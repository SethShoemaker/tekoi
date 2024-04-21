import typing as _typing
from tekoi.framework import (Request as _Request, 
                             Response as _Response,
                             PipelineMember as _PipelineMember)
from .storage import (SessionStorageProtocol as _SessionStorageProtocol)


class Handler(_PipelineMember):

    def __init__(self, session_storage: _SessionStorageProtocol) -> None:
        self.session_storage = session_storage
        self.session_cookie_name = "SESSION"

    def __call__(self, request: _Request, next: _typing.Callable[[_Request], _Response]) -> _Response:

        session_cookie = request.cookies.get(self.session_cookie_name) if request.cookies is not None else None

        if session_cookie is not None:
            request.sessions_session_data = self.session_storage.get_session_data(session_cookie.value)

        res = next(request)

        if session_cookie is None:
            new_session_id = self.session_storage.create_session({})
            res.cookies.set(self.session_cookie_name, new_session_id)

        return res
