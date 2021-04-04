import functools
import logging
from typing import Any, Callable, Dict, List, Union

from asyncpg.connection import Connection as Conn
from asyncpg.pool import Pool
from discord.ext.commands import Context

log = logging.getLogger(__name__)


def connection_pool_accessor(func: Callable) -> Any:
    """Giving a method a connection to a database from a connection pool."""

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
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
    async def select(
        self,
        *,
        table: str,
        fields: Union[List[str], str] = "*",
        info: Dict[str, Any],
        conn: Conn,
    ) -> list:
        """Select from the database."""
        selection_fields = f"({', '.join(fields)})" if isinstance(fields, list) else fields

        key_fields = ("WHERE " if len(info) else "") + (
            " AND ".join(f"{k} = ${i}" for i, k in enumerate(info.keys()))
        )

        return await conn.fetch(f"SELECT {selection_fields} FROM {table} {key_fields}", *info.values())

    @connection_pool_accessor
    async def insert(self, *, table: str, info: Dict[str, Any], conn: Conn) -> None:
        """Insert into the database."""
        key_fields = ", ".join(info.keys())
        value_numbers = ", ".join(f"${i}" for i in range(1, len(info) + 1))

        await conn.execute(
            f"INSERT INTO {table.upper()}({key_fields}) VALUES ({value_numbers})", *info.values()
        )

    @connection_pool_accessor
    async def delete(self, *, table: str, info: Dict[str, Any], conn: Conn) -> None:
        """Delete from the database."""
        key_fields = " AND ".join(f"{k} = ${i}" for i, k in enumerate(info.keys()))

        await conn.execute(f"DELETE FROM {table} WHERE {key_fields}", *info.values())

    async def check_if_blocked(self, ctx: Context) -> bool:
        """Checks if user/guild is blocked."""
        user = await self.select(table="Blocked_Users", info={"user_id": ctx.author.id})

        if not len(user):
            # If the user is not blocked, check if the guild is blocked.
            guild = await self.select(table="Blocked_Guilds", info={"guild_id": ctx.guild.id})

            if not len(guild):
                return True

        # If none of the checks passed, either the guild or the user is blocked.
        return False
