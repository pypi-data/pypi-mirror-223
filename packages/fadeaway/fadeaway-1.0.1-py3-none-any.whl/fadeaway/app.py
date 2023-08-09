from werkzeug.routing import Map, Rule, MapAdapter
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.exceptions import HTTPException
from werkzeug.routing.exceptions import RequestRedirect
from contextvars import Token

import typing as t
from .response import make_response
from .context import Context, _cv
from .config import Config
from .middleware import MiddleWare
from .blueprint import Blueprint


T_String = str
T_Int = int
T_Bool = bool
T_Bytes = bytes
T_ByteArray = bytearray
T_NoReturn = t.NoReturn

T_Config = Config
T_Context = Context
T_CV_Token = t.Optional[Token]
T_Middleware = MiddleWare
T_Blueprint = Blueprint
T_Request = Request
T_Response = Response
T_RawResponse = t.Union[
    t.Tuple[T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray, T_Int],
    T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray]
T_RealResponse = t.Iterable[T_Bytes]
T_HTTPMethods = t.Union[t.Tuple[T_String, ...], t.List[T_String], None]
T_Rule = Rule
T_UrlMap = Map
T_Adapter = MapAdapter
T_ViewFunction = t.Callable[[T_Context], T_RawResponse]
T_ViewFunctions = t.Dict[T_String, T_ViewFunction]
T_BeforeRequestFunction = t.Callable[[T_Context], None]
T_BeforeRequestFunctions = t.List[T_BeforeRequestFunction]
T_AfterRequestFunction = t.Callable[[T_Context], None]
T_AfterRequestFunctions = t.List[T_AfterRequestFunction]
T_RouteMethod = t.Callable[[T_ViewFunction], T_ViewFunction]
T_ErrorHandler = t.Callable[[HTTPException], T_RawResponse]
T_ErrorHandlers = t.Dict[T_Int, T_ErrorHandler]


class FadeAway(object):

    def __init__(self):
        self.config: T_Config = Config()
        self._url_map: T_UrlMap = Map()
        self._view_funcs: T_ViewFunctions = {}
        self._before_request_funcs: T_BeforeRequestFunctions = []
        self._after_request_funcs: T_AfterRequestFunctions = []
        self._error_handlers: T_ErrorHandlers = {}

    def dispatch_request(self, request: T_Request) -> T_Response:
        ctx: T_Context = Context()
        _cv_token: T_CV_Token = None
        adapter: T_Adapter = self._url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            ctx.set("request", request)
            ctx.set("current_app", self)
            _cv_token = _cv.set(ctx)
            for f in self._before_request_funcs:
                f(ctx)
            response: T_Response = make_response(self._view_funcs[endpoint](ctx))
            ctx.set("response", response)
            for f in self._after_request_funcs:
                f(ctx)
        except RequestRedirect as e:
            ctx.set("response", e.get_response())
        except HTTPException as e:
            if self._error_handlers.get(e.code) is not None:
                response = make_response(self._error_handlers.get(e.code)(e))
            else:
                response = e.get_response()
            ctx.set("response", response)
        finally:
            if _cv_token is not None:
                _cv.reset(_cv_token)
        return ctx.response

    def wsgi_app(self, environ, start_response) -> T_RealResponse:
        request: T_Request = Request(environ)
        response: T_Response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response) -> T_RealResponse:
        return self.wsgi_app(environ, start_response)

    def before_request(self, func: T_BeforeRequestFunction):
        self._before_request_funcs.append(func)
        return func

    def after_request(self, func: T_AfterRequestFunction):
        self._after_request_funcs.append(func)
        return func

    def use(self, middleware: T_Middleware):
        self._before_request_funcs.append(middleware.before)
        self._after_request_funcs.insert(0, middleware.after)

    def route(self,
              rule: T_String,
              methods: T_HTTPMethods = None) -> T_RouteMethod:
        if methods is None:
            methods = ("GET",)

        def decorator(view_func: T_ViewFunction) -> T_ViewFunction:
            self.add_url_rule(rule, view_func.__name__, methods, view_func)
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
        self._url_map.add(rule)
        self._view_funcs[endpoint] = view_func

    def register_blueprint(self, blueprint: Blueprint):
        for rule in blueprint.rules:
            self.add_url_rule(blueprint.url_prefix + rule.rule,
                              rule.endpoint, rule.methods, blueprint.view_funcs[rule.endpoint])

    def register_error_handler(self, code: T_Int, error_handler: T_ErrorHandler) -> T_NoReturn:
        self._error_handlers[code] = error_handler

    def error_handler(self, code: T_Int):
        def decorator(e_handler: T_ErrorHandler) -> T_ErrorHandler:
            self._error_handlers[code] = e_handler
            return e_handler
        return decorator

    def run(self,
            host: T_String = "localhost",
            port: T_Int = 5000,
            debug: T_Bool = True,):
        run_simple(hostname=host, port=port, application=self, use_debugger=debug, use_reloader=debug)
