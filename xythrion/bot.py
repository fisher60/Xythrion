import asyncio
import logging
from datetime import datetime
from typing import Coroutine, Optional

import aiohttp
import asyncpg
from discord import Message
from discord.ext import commands

from xythrion import Context
from xythrion.constants import Postgresql
from xythrion.databasing import Database

log = logging.getLogger(__name__)


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        self.startup_time = datetime.now()

        self.pool: Optional[asyncpg.pool.Pool] = None
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.db: Optional[Database] = None

        self.add_check(self.check_if_blocked)

    async def check_if_blocked(self, ctx: Context) -> bool:
        """If user and/or guild is blocked, no commands by this bot can be ran."""
        user = await self.db.select(table="blocked_users", info={"user_id": ctx.author.id})

        if not len(user):
            # If the user is not blocked, check if the guild is blocked.
            guild = await self.db.select(table="blocked_guilds", info={"guild_id": ctx.guild.id})

            if not len(guild):
                return True

        # If none of the checks passed, either the guild or the user is blocked.
        return False

    async def get_context(self, message: Message, *, cls: commands.Context = Context) -> Coroutine:
        """Creating a custom context so new methods can be made for quality of life changes."""
        return await super().get_context(message, cls=cls)

    async def request(self, url: str, **kwargs) -> dict:
        """Requesting from a URl."""
        async with self.http_session.get(url, **kwargs) as response:
            assert response.status == 200, f"Could not request from URL. Status {response.status}."

            return await response.json()

    async def post(self, url: str, **kwargs) -> dict:
        """Posting to a URL."""
        async with self.http_session.post(url, **kwargs) as response:
            assert response.status == 200, f"Could not post to URL. Status {response.status}."

            return await response.json()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.trace("Awaiting...")

    async def login(self, *args, **kwargs) -> None:
        """Creating all the important connections."""
        self.pool = asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60, loop=self.loop)

        log.trace("Successfully connected to Postgres database.")

        self.http_session = aiohttp.ClientSession()

        self.db = Database(self.pool)

        await super().login(*args, **kwargs)

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.pool.close(), self.http_session.close()}, loop=self.loop, timeout=30.0)

        log.trace("Finished closing task(s).")

        return await super().logout()
