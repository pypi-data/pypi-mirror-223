from typing import Self, TypeVar, Any

from flask import g
import sqlalchemy
from sqlalchemy.engine import Engine

from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase

from nsj_flask_utils.daos     import BaseDAO
from nsj_flask_utils.services import BaseService

TDAO = TypeVar('TDAO', bound=BaseDAO)
TSER = TypeVar('TSER', bound=BaseService)


def _create_pool(db_url: str) -> Engine:
    db_pool = sqlalchemy.create_engine(
        db_url,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    return db_pool


def _get_ext_db_url() -> str:
    ext_db: dict[str, str] = g.external_database
    return f'postgresql+pg8000://{ext_db["user"]}:{ext_db["password"]}@{ext_db["host"]}:{ext_db["port"]}/{ext_db["name"]}'


def _create_ext_pool() -> Engine:
    ext_db_url : str    = _get_ext_db_url()
    ext_db_pool: Engine = _create_pool(ext_db_url)
    return ext_db_pool


class InjectorFactory(NsjInjectorFactoryBase):
    def __enter__(self) -> Self:
        pool = _create_ext_pool()
        self._db_conn = pool.connect()
        return self

    def __exit__(self, *_: Any) -> None:
        self._db_conn.close()
        pass

    def create_dao(self, dao: type[TDAO]) -> TDAO:
        return dao(self._db_conn)

    def create_service(self, service: type[TSER]) -> TSER:
        return service(self._db_conn)

