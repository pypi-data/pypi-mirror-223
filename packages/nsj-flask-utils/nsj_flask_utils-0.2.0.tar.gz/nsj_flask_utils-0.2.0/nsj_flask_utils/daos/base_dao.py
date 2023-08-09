from typing import Generic, Any, Mapping, Generic, TypeVar

import sqlalchemy
from flask_sqlalchemy    import SQLAlchemy
from sqlalchemy.engine   import Connection, CursorResult, Transaction

from nsj_flask_utils.dtos.base_dto      import BaseDTO
from nsj_flask_utils.utils.request_args import RequestArgs

TDTO = TypeVar('TDTO', bound=BaseDTO)


class BaseDAO(Generic[TDTO]):
    _db : Connection | SQLAlchemy
    _dto: type[TDTO]

    def __init__(self, db : Connection | SQLAlchemy
                     , dto: type[TDTO] | None = None) -> None:
        self._db = db
        if dto:
            self._dto = dto
            pass
        pass

    def _execute(self, query: str
                     , params: Mapping[str, Any] = {}) -> CursorResult[Any]:
        if isinstance(self._db, Connection):
            tran: Transaction = self._db.begin()
            rs = self._db.execute(sqlalchemy.text(query), params)
            tran.commit()
            return rs
        return self._db.execute(sqlalchemy.text(query), params)

    def _get_ftbl_name(self) -> str:
        """Returns the table name formatede: `schema.tbl_name'"""
        return f"{self._dto.__schema__}.{self._dto.__table_name__}"

    def _list(self, query: str
                  , pagi_args: dict[str, str | int]
                  , filter_args: dict[str, str]
                  , group_by: str | None = None
                  , special_map: dict[str, str] = {}) -> list[TDTO]:
        query = self._filter_query(query, filter_args, group_by, special_map)

        if group_by:
            query += f"\nGROUP BY {group_by}"
            pagi_args['order_by'] = group_by
            pass

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

    def get(self, id: Any) -> TDTO | None:
        query: str = f"SELECT * FROM {self._get_ftbl_name()}"
        filter_args = {self._dto.__PK__: id}
        query = self._filter_query(query, filter_args)
        rs = self._execute(query, filter_args).mappings().first()
        if not rs:
            return None
        return self._dto(**rs)

    def _filter_query(self, query: str
                          , filter_args: dict[str, str]
                          , group_by: str | None = None
                          , special_map: dict[str, str] = {}) -> str:
        def sp_get(k: str) -> str:
            return special_map.get(k, k)

        keys = list(filter_args.keys())

        if group_by:
            query += f"\nWHERE {group_by} IS NOT NULL"
            pass

        if keys:
            if not group_by:
                query += f"\nWHERE {sp_get(keys[0])} = :{keys[0]}"
                keys.pop(0)
                pass
            for key in keys:
                query += f"\n  AND {sp_get(key)} = :{key}"
                pass
            pass
        return query

    def _get_first(self, query: str
                       , filter_args: dict[str, str]) -> Any | None:
        rs = self._execute(query, filter_args)
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

    def list(self, req_args: RequestArgs) -> list[TDTO]:
        query: str = f"SELECT * FROM {self._get_ftbl_name()}"
        return self._list(query, req_args.get_pagination_params()
                               , req_args.get_filter_params())

    def get_rows_total(self, req_args: RequestArgs
                           , special_map: dict[str, str] = {}) -> int:
        filter_args = req_args.get_filter_params()

        query: str = f"SELECT COUNT(*) FROM {self._get_ftbl_name()}"

        gb: str | None = req_args.group_by
        if gb:
            query = f"SELECT COUNT(DISTINCT {gb}) FROM {self._get_ftbl_name()}"
            pass
        query = self._filter_query(query, filter_args, gb, special_map)

        ret = self._get_first(query, filter_args)
        if not ret:
            return -1
        return int(ret)
