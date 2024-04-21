class RequestCookie:

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

class RequestCookieCollection:

    def __init__(self, items: list[RequestCookie]) -> None:
        self.items_list = items
        self.items_dict = {cookie.name: cookie for cookie in items}

    def get(self, cookie_name: str) -> RequestCookie|None:
        return self.items_dict.get(cookie_name)

class Request:

    method: str|None = None
    path: str|None = None
    cookies: RequestCookieCollection|None = None
