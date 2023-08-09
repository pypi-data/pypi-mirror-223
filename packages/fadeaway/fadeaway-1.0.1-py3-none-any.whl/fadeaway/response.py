from werkzeug.wrappers import Response
from werkzeug.utils import redirect
import json
import typing as t


T_String = str
T_Int = int
T_Bytes = bytes
T_ByteArray = bytearray
T_Response = Response
T_RawResponse = t.Union[
    t.Tuple[T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray, T_Int],
    T_Response, t.Dict, t.List, T_String, T_Bytes, T_ByteArray]


def make_response(return_value: T_RawResponse) -> T_Response:
    status = None
    headers = None
    if isinstance(return_value, tuple):
        if len(return_value) == 2:
            return_value, status = return_value
    if not isinstance(return_value, Response):
        if isinstance(return_value, (dict, list)):
            return_value = jsonify(return_value, status=status, headers=headers)
        if isinstance(return_value, (str, bytes, bytearray)):
            return_value = Response(return_value, status=status, headers=headers)
    return return_value


class jsonify(Response):
    def __init__(self, obj=None, status=None, headers=None):
        super().__init__(json.dumps(obj), status=status, headers=headers, content_type="application/json")
