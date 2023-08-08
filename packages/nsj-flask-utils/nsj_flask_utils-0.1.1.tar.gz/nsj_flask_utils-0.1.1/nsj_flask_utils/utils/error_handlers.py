from typing import Any

from flask import Flask, Response
from werkzeug.exceptions import HTTPException

from nsj_flask_utils.utils      import json
from nsj_flask_utils.exceptions import HTTPBaseException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def http_exception_handler(e: HTTPException) -> Response:
        """Return JSON instead of HTML for HTTP errors."""
        eres = e.get_response()
        response = Response(None, eres.status_code, eres.headers
                                , eres.mimetype, eres.content_type)
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(HTTPException)
    def http_base_exception_handler(e: HTTPBaseException) -> tuple[str, int]:
        """Return JSON instead of HTML for HTTP errors."""
        return e.to_tuple_str_int()
    pass
