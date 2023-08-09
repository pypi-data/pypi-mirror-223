import math
from typing import Any, Generic, List, TypeVar

from sqlalchemy.engine   import Connection
from werkzeug.exceptions import NotFound

from nsj_flask_utils.utils import RequestArgs
from nsj_flask_utils.daos  import BaseDAO
from nsj_flask_utils.dtos  import BaseDTO

TDTO = TypeVar('TDTO', bound=BaseDTO)
TDAO = TypeVar('TDAO', bound=BaseDAO)


class BaseService(Generic[TDAO, TDTO]):
    _dao_cls: type[TDAO]
    _dto_cls: type[TDTO]

    _dao: TDAO
    _dto: type[TDTO]

    def __init__(self, db : Connection
                     , dao: type[TDAO] | None = None
                     , dto: type[TDTO] | None = None) -> None:
        if dao:
            self._dao = dao(db)
        elif self._dao_cls:
            self._dao = self._dao_cls(db)
        else:
            raise Exception('DAO not defined')

        if dto:
            self._dto = dto
        elif self._dto_cls:
            self._dto = self._dto_cls
        else:
            raise Exception('DTO not defined')
        pass

    def list(self, req_args: RequestArgs) -> list[TDTO]:
        return self._dao.list(req_args)

    def create(self, dto: TDTO) -> TDTO:
        return self._dao.create(dto)

    def get_or_none(self, id: Any) -> TDTO | None:
        return self._dao.get(id)

    def get_or_raise(self, id: Any
                         , exception: type[Exception] = NotFound) -> TDTO:
        rs = self._dao.get(id)
        if not rs:
            raise exception("Not found")
        return rs

    def update(self, id: Any, dto: TDTO) -> TDTO:
        original = self.get_or_raise(id)
        atualizado = original.model_copy(
            update=dto.model_dump(exclude_unset=True)
        )
        self._dao.update(atualizado)
        return atualizado

    def delete(self, id: Any) -> TDTO:
        self.get_or_raise(id)
        return self._dao.delete(id)

    def paginate_response(self, req_args: RequestArgs
                              , data    : List[TDTO]
                              , exclude : set[str] | None = None
                              , include : set[str] | None = None) -> dict[str, Any]:
        rows_total = self._dao.get_rows_total(req_args)
        pagination_params = req_args.get_pagination_params()
        current_page = int(pagination_params["page"])
        total_pages = math.ceil(rows_total / int(pagination_params["limit"]))

        next_page: int | None = None
        if current_page < total_pages:
            next_page = current_page + 1
            pass

        prev_page: int | None = None
        if current_page != 1:
            prev_page = current_page - 1
            pass

        if include:
            ndata = [model.model_dump(include=include) for model in data]
        elif exclude:
            ndata = [model.model_dump(exclude=exclude) for model in data]
        else:
            ndata = [model.model_dump() for model in data]

        response = {
            "total": rows_total,
            "next_page": next_page,
            "current_page": current_page,
            "total_pages": total_pages,
            "prev_page": prev_page,
            "data": ndata,
        }

        return response
