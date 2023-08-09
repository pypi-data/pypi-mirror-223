from typing import Any

import nsj_flask_utils.utils.json as json


class HTTPBaseException(Exception):
    data: dict[str, Any]
    code: int

    def __init__(self,data: dict[str, Any]) -> None:
        self.data = data

    @classmethod
    def message(cls: type['HTTPBaseException'],
                message: str) -> 'HTTPBaseException':
        return cls({'message': message})

    def to_tuple(self) -> tuple[dict[str, Any], int]:
        return (self.data, self.code)

    def to_tuple_str_int(self) -> tuple[str, int]:
        return (json.dumps(self.data), self.code)


class HTTP400(HTTPBaseException):
    code = 400
