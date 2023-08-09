from werkzeug.wrappers import Request, Response
from contextvars import ContextVar
import typing as t

T_String = str
T_Any = t.Any
T_NoReturn = t.NoReturn
T_Global = t.Dict[T_String, T_Any]
T_Request = t.Optional[Request]
T_Response = t.Optional[Response]


class Context(object):
    def __init__(self):
        self._g: T_Global = dict()
        self.request: T_Request = None
        self.current_app = None
        self.response: T_Response = None

    def set(self, key: T_String, value: T_Any) -> T_NoReturn:
        if key in ("request", "current_app", "response"):
            self.__dict__[key] = value
        else:
            self._g[key] = value

    def get(self, key: T_String) -> T_Any:
        return self._g.get(key)

    def __getattr__(self, key: T_String) -> T_Any:
        return self._g.get(key)

    def __setattr__(self, key: T_String, value: T_Any) -> T_NoReturn:
        if key == "_g":
            self.__dict__[key] = value
        else:
            self.set(key, value)

    @property
    def g(self) -> T_Global:
        return self._g


_cv: ContextVar[Context] = ContextVar("_cv")
