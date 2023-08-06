from typing import Literal

from pydantic import BaseModel, StrictStr

from nsj_flask_utils.dtos.base_dto import BaseDTO


class PaginationDTO(BaseModel):
    order: Literal['ASC', 'DESC'] = 'DESC'
    order_by: StrictStr = ''
    page: int = 1
    limit: int = 20


class PaginationParams:
    data: PaginationDTO
    offset: int

    def __init__(self, dto_cls: type[BaseDTO]
                     , data: PaginationDTO) -> None:
        self.data = data
        self.offset = data.limit * (data.page - 1)

        if not data.order_by:
            self.order_by = dto_cls.__order_by__
        elif data.order_by in dto_cls.model_fields.keys():
            self.order_by = data.order_by
        else:
            self.order_by = dto_cls.__order_by__
            pass
        pass

    def to_dict(self) -> dict[str, str | int]:
        return {
            "limit": self.data.limit,
            "offset": self.offset,
            "order_by": self.order_by,
            "order": self.data.order,
            "page": self.data.page,
        }
    pass
