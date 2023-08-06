from typing import Any

from pydantic                import ValidationError
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions     import BadRequest

from nsj_flask_utils.dtos.base_dto import BaseDTO
from nsj_flask_utils.exceptions    import HTTP400

from .filter_params     import FilterParams
from .pagination_params import PaginationParams, PaginationDTO

class RequestArgs:
    filter_params: FilterParams
    pagi_params  : PaginationParams

    def __init__(self, dto_cls: type[BaseDTO]
                     , args   : MultiDict[str, str]) -> None:
        (obj_fields, pagi_dto) = self._validate(dto_cls, args)
        self.filter_params = FilterParams(obj_fields)
        self.pagi_params   = PaginationParams(
            dto_cls, pagi_dto
        )
        pass

    def _validate(self, dto_cls: type[BaseDTO]
                      , args: MultiDict[str, str]) -> tuple[dict[str, Any], PaginationDTO]:
        obj_fields_name : list[str] = list(dto_cls.model_fields.keys())
        pagi_fields_name: list[str] = list(PaginationDTO.model_fields.keys())

        # Possible Fields
        p_fields: list[str] = []
        p_fields.extend(obj_fields_name)
        p_fields.extend(pagi_fields_name)

        for k in args.keys():
            if not k in p_fields:
                if k != 'tenant':
                    raise BadRequest(f"Field {k} isn't a valid field.")
            pass

        obj_fields: dict[str, Any] = {
            k: v
            for k, v in args.items()
            if k in obj_fields_name
        }

        try:
            dto_cls.validate(obj_fields)
        except ValidationError as e:
            errs = {
                x['loc'][0]: x['msg']
                for x in e.errors()
            }
            matchs: list[str] = [
                x
                for x in args.keys()
                if x in errs
            ]

            if matchs:
                errdict = {
                    k: v
                    for k, v in errs.items()
                    if k in matchs
                }
                raise HTTP400({
                    'message': 'Invalid filter params',
                    'erros': errdict,
                })

        pagi_fields: dict[str, Any] = {
            k: v
            for k, v in args.items()
            if k in pagi_fields_name
        }

        pagi_dto: PaginationDTO
        try:
            pagi_dto = PaginationDTO(**pagi_fields)
        except ValidationError as e:
            errs = {
                x['loc'][0]: x['msg']
                for x in e.errors()
            }
            raise HTTP400({
                'message': 'Invalid filter params',
                'erros': errs
            })

        return obj_fields, pagi_dto

    def get_filter_params(self) -> dict[str, str]:
        return self.filter_params.__dict__

    def get_pagination_params(self) -> dict[str, str | int]:
        return self.pagi_params.to_dict()
