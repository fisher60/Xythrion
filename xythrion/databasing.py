from __future__ import annotations

import functools
import logging
from typing import Any, Callable, Dict, List, NoReturn

from async_lru import alru_cache
from asyncpg.connection import Connection as Conn
from asyncpg.pool import Pool

from xythrion.constants import Config

log = logging.getLogger(__name__)


def connection_pool_accessor(func: Callable) -> Any:
    """Giving a method a connection to a database from a connection pool."""

    @alru_cache(maxsize=Config.CACHE_BACKWARDS_COUNT)
    @functools.wraps(func)
    async def wrapper(self: Database, *args, **kwargs) -> None:
        async with self.pool.acquire() as conn:
            if kwargs["conn"] is None:
                kwargs["conn"] = conn

            await func(*args, **kwargs)

    return wrapper


class Database:
    """Utilities for the Postgres database."""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool

    @connection_pool_accessor
    async def select(self, *, table: str, fields: List[str] = "*", info: Dict[str, Any], conn: Conn) -> list:
        """Select from the database."""
        selection_fields = f"({', '.join(fields)})"
        key_fields = "WHERE " if len(info) else ""
        conditional_fields = " AND ".join(f"{k} = ${i}" for i, k in enumerate(info.keys()))

        return await conn.fetch(
            f"SELECT {selection_fields} FROM {table} {key_fields + conditional_fields}", *info.values())

    @connection_pool_accessor
    async def insert(self, *, table: str, info: Dict[str, Any], conn: Conn) -> None:
        """Insert into the database."""
        key_fields = ", ".join(info.keys())
        value_numbers = ", ".join(f"${i}" for i in range(1, len(info) + 1))

        await conn.execute(
            f"INSERT INTO {table.upper()}({key_fields}) VALUES ({value_numbers})", *info.values())

    @connection_pool_accessor
    async def delete(self, *, table: str, info: Dict[str, Any], conn: Conn) -> None:
        """Delete from the database."""
        key_fields = " AND ".join(f"{k} = ${i}" for i, k in enumerate(info.keys()))

        await conn.execute(f"DELETE FROM {table} WHERE {key_fields}", *info.values())

    @connection_pool_accessor
    async def update(self, *, table: str, info: Dict[str, Any], conn: Conn) -> NoReturn:
        """Updates a record in the database with new information."""
        raise NotImplementedError
