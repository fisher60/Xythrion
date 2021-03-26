import logging
from typing import Any, Callable, Dict

from asyncpg.connection import Connection
from asyncpg.pool import Pool
from discord.ext.commands import Context

log = logging.getLogger(__name__)


class Database:
    """Utilities for the database, inheriting from setup."""

    def __init__(self, pool: Pool) -> None:
        self.pool = pool

    async def connection_pool_accessor(self, func: Callable) -> Any:

        async def wrapper(*args, **kwargs):
            async with self.pool.acquire() as conn:
                await func(conn, *args, **kwargs)

        return wrapper

    @connection_pool_accessor
    async def insert(self, conn: Connection, table: str, info: Dict[str, Any]) -> None:
        """Insert into the database."""
        key_fields = ", ".join(info.keys())
        value_numbers = ", ".join(f"${i}" for i in range(1, len(info) + 1))

        await conn.execute(
            f"INSERT INTO {table.upper()}({key_fields}) VALUES ({value_numbers})", *info.values()
        )

    @connection_pool_accessor
    async def select(self, conn: Connection) -> None:
        """Select from the database."""
        pass

    @connection_pool_accessor
    async def delete(self, conn: Connection) -> None:
        """Delete from the database."""
        pass

    @connection_pool_accessor
    async def check_if_blocked(self, conn: Connection, ctx: Context) -> bool:
        """Checks if user/guild is blocked."""
        user = await conn.fetch("SELECT * FROM Blocked_Users WHERE user_id = $1", ctx.author.id)

        if not len(user):
            # If the user is not blocked, check if the guild is blocked.
            guild = await conn.fetch("SELECT * FROM Blocked_Guilds WHERE guild_id = $1", ctx.guild.id)

            if not len(guild):
                return True

        # If none of the checks passed, either the guild or the user is blocked.
        return False
