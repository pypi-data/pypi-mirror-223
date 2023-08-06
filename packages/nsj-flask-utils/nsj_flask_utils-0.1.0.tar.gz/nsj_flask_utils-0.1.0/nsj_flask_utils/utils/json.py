import json as _json

from datetime import datetime, date
from typing   import Any

def _default(o: Any) -> str:
    return {
        datetime: lambda o: o.strftime('%Y-%m-%d %H:%M:%S'),
        date    : lambda o: o.strftime('%Y-%m-%d')
    }.get(type(o), str)(o)


def dumps(*args: Any, **kwargs: Any) -> str:
    if not 'default' in kwargs:
        kwargs['default'] = _default
        pass
    return _json.dumps(*args, **kwargs)
