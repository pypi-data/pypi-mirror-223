from typing import ClassVar

from pydantic import BaseModel


class BaseDTO(BaseModel):
    __order_by__  : ClassVar[str]
    __table_name__: ClassVar[str]
    __schema__    : ClassVar[str]
    __PK__        : ClassVar[str]
    pass
