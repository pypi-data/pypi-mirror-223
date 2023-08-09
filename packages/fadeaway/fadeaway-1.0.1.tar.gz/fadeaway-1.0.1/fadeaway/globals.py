from werkzeug.local import LocalProxy
from .context import _cv
from .app import FadeAway

current_app: FadeAway = LocalProxy(
    _cv, "current_app"
)
