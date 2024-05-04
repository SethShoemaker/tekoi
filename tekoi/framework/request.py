from typing import Any as _Any
from tekoi.core import startup as _startup

class Request(_startup.Request):

    routing_target: _Any = None

    routing_path_params: dict[str, str]| None = None

    sessions_session_data: _Any = None
