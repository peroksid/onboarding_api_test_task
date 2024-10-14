from functools import lru_cache

from psycopg_pool import ConnectionPool, AsyncConnectionPool

from .config import get_settings


@lru_cache()
def get_conninfo():
    settings = get_settings()
    return f"user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} dbname={settings.db_name}"


@lru_cache()
def get_pool():
    return ConnectionPool(conninfo=get_conninfo())


@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=get_conninfo())
