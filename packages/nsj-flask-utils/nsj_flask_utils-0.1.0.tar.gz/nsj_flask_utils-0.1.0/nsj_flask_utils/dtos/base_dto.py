from typing import ClassVar

from pydantic import BaseModel

class BaseDTO(BaseModel):
    __order_by__  : ClassVar
    __table_name__: ClassVar
    __schema__    : ClassVar
    __PK__        : ClassVar
    pass
