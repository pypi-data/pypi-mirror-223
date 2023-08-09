from werkzeug.routing import Rule
from werkzeug.wrappers import Response
import typing as t
from .context import Context

T_String = str
T_Int = int
T_Bytes = bytes
T_ByteArray = bytearray

T_Response = Response
T_RawResponse = t.Union[
    t.Tuple[T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray, T_Int],
    T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray]
T_Context = Context

T_Rule = Rule
T_Rules = t.List[Rule]

T_HTTPMethods = t.Union[t.Tuple[T_String, ...], t.List[T_String], None]
T_ViewFunction = t.Callable[[T_Context], T_RawResponse]
T_ViewFunctions = t.Dict[T_String, T_ViewFunction]
T_RouteMethod = t.Callable[[T_ViewFunction], T_ViewFunction]


class Blueprint(object):
    def __init__(self, name: T_String, url_prefix: T_String):
        self.name: T_String = name
        self.url_prefix: T_String = url_prefix
        self._rules: T_Rules = list()
        self._view_funcs: T_ViewFunctions = dict()

    def route(self,
              rule: T_String,
              methods: T_HTTPMethods = None) -> T_RouteMethod:
        if methods is None:
            methods = ("GET",)

        def decorator(view_func: T_ViewFunction) -> T_ViewFunction:
            self.add_url_rule(rule, f"{self.name}.{view_func.__name__}", methods, view_func)
            return view_func

        return decorator

    def add_url_rule(self,
                     rule: T_String,
                     endpoint: T_String,
                     methods: T_HTTPMethods,
                     view_func: T_ViewFunction):

        old_func = self._view_funcs.get(endpoint)
        if old_func is not None and old_func != view_func:
            raise AssertionError(
                "View function mapping is overwriting an existing"
                f" endpoint function: {endpoint}"
            )

        rule: T_Rule = Rule(rule, endpoint=endpoint, methods=methods)
        self._rules.append(rule)
        self._view_funcs[endpoint] = view_func

    @property
    def rules(self):
        return self._rules

    @property
    def view_funcs(self):
        return self._view_funcs
