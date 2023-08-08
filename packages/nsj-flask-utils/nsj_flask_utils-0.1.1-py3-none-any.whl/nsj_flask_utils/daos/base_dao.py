from typing import Generic, Any, Mapping, Generic, TypeVar

import sqlalchemy
from werkzeug.exceptions import NotFound
from sqlalchemy.engine   import Connection, CursorResult, Transaction

from nsj_flask_utils.dtos.base_dto import BaseDTO

TDTO = TypeVar('TDTO', bound=BaseDTO)

class BaseDAO(Generic[TDTO]):
    _db : Connection
    _dto: type[TDTO]

    def __init__(self, db : Connection
                     , dto: type[TDTO] | None = None) -> None:
        self._db = db
        if dto:
            self._dto = dto
            pass
        pass

    def _execute(self, query: str
                     , params: Mapping[str, Any] = {}) -> CursorResult[Any]:
        tran: Transaction = self._db.begin()
        rs = self._db.execute(sqlalchemy.text(query), params)
        tran.commit()
        return rs

    def _get_ftbl_name(self) -> str:
        """Returns the table name formatede: `schema.tbl_name'"""
        return f"{self._dto.__schema__}.{self._dto.__table_name__}"


    def _list(self, query: str, pagi_args  : dict[str, str | int]
                              , filter_args: dict[str, str]) -> list[TDTO]:
        query = self._filter_query(query, filter_args)

        query += f"""
ORDER BY {pagi_args['order'],} {pagi_args['order_by'],}
LIMIT :limit
OFFSET :offset
"""

        params = {
            **pagi_args,
            **filter_args,
        }

        rs = self._execute(query, params)
        return [
            self._dto(**x)
            for x in rs.mappings().all()
        ]

    def _get(self, query: str, params: dict[str, Any]) -> TDTO:
        rs = self._execute(query, params).mappings().first()
        if not rs:
            raise NotFound('Evento Not Found')
        return self._dto(**rs)

    def get(self, id: str) -> TDTO:
        query: str = f"SELECT * FROM {self._get_ftbl_name()}"
        filter_args = {self._dto.__PK__: id}
        query = self._filter_query(query, filter_args)
        return self._get(query, filter_args)

    def _filter_query(self, query: str, filter_args: dict[str, str]) -> str:
        keys = list(filter_args.keys())
        if keys:
            query += f" WHERE {keys[0]} = :{keys[0]}"
            keys.pop(0)
            for key in keys:
                query += f" AND {key} = :{key}"
        return query

    def _get_first(self, query: str) -> Any | None:
        rs = self._execute(query)
        frow = rs.first()
        if not frow:
            return None
        return frow[0]

    def get_all(self) -> list[TDTO]:
        query: str = f"SELECT * FROM {self._get_ftbl_name()}"
        rs = self._execute(query)
        return [
            self._dto(**x)
            for x in rs.mappings().all()
        ]

    def list(self, pagi_args   : dict[str, str | int]
                 , filter_args : dict[str, str] = {}) -> list[TDTO]:
        query: str = f"SELECT * FROM {self._get_ftbl_name()}"
        return self._list(query, pagi_args, filter_args)

    def get_rows_total(self) -> int:
        query: str = f"SELECT count(*) FROM {self._get_ftbl_name()}"
        ret = self._get_first(query)
        if not ret:
            return -1
        return int(ret)
