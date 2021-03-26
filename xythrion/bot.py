import asyncio
import logging
from datetime import datetime
from typing import Optional

import aiohttp
import asyncpg
from discord.ext.commands import Bot

from xythrion.constants import Postgresql
from xythrion.databasing import Database

log = logging.getLogger(__name__)


class Xythrion(Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        self.startup_time = datetime.now()

        self.pool: Optional[asyncpg.pool.Pool] = None
        self.http_session: Optional[aiohttp.ClientSession] = None

        self.database = Database(self.pool)

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.trace("Awaiting...")

    async def login(self, *args, **kwargs) -> None:
        """Creating all the important connections."""
        try:
            self.pool = asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60, loop=self.loop)

            log.trace("Successfully connected to Postgres database.")

        except Exception as e:
            log.error("Failed to connect to Postgresql database", exc_info=(type(e), e, e.__traceback__))

        self.http_session = aiohttp.ClientSession()

        await super().login(*args, **kwargs)

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.pool.close(), self.http_session.close()}, loop=self.loop, timeout=30.0)

        log.trace("Finished closing task(s).")

        return await super().logout()
