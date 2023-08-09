from .context import Context

T_Context = Context


class MiddleWare(object):
    def before(self, ctx: T_Context) -> None:
        raise NotImplementedError

    def after(self, ctx: T_Context) -> None:
        raise NotImplementedError
