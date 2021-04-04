import asyncio
import functools
import logging
from abc import ABC
from datetime import datetime
from typing import Any, Awaitable, Callable, Optional

import aiohttp
import asyncpg
from discord.ext.commands import Bot, Context

from xythrion.constants import Config, Postgresql
from xythrion.databasing import Database
from xythrion.network import Network

log = logging.getLogger(__name__)


class CustomAbstractEventLoop(asyncio.AbstractEventLoop, ABC):
    """Giving the abstract event loop more methods."""

    @staticmethod
    async def run_in_executor(func: Callable, *args: Optional[Any], executor: Optional[Any] = None) -> Awaitable:
        """Executor is never used. Defaulting to None."""
        return super().run_in_executor(executor, func, *args)

    async def graph_executor(self, func: Callable, calculate_func: Optional[Callable] = None) -> Any:
        """
        Method for computing stuff before the call to the executor to run the plotting method.

        The computation function will not be ran if it doesn't exist.

        I wouldn't look at this too closely. I programmed it at 3am.
        """
        f_calculate_func = None if calculate_func is None else self.run_in_executor(calculate_func)

        try:
            if f_calculate_func is None:
                return await asyncio.wait_for(self.run_in_executor(func), Config.COMPUTATION_TIMEOUT, loop=self)
            else:
                computation_result = await asyncio.wait_for(f_calculate_func, Config.COMPUTATION_TIMEOUT, loop=self)
                f_func = functools.partial(func, computation_result)
                return await asyncio.wait_for(f_func, Config.COMPUTATION_TIMEOUT, loop=self)

        except asyncio.TimeoutError:
            log.warning(f"Plotting could not finish in {Config.COMPUTATION_TIMEOUT} seconds. Aborting.")


class CustomContext(Context):
    """Customization of methods for context."""

    async def send(self, *args, **kwargs) -> None:
        """
        The same as the regular send function, but returns nothing.

        This is useful for having a return statement along with a send function on the same line.
        """
        await super().send(*args, **kwargs)


class Xythrion(Bot, CustomAbstractEventLoop, ABC):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super(Xythrion, self).__init__(*args, **kwargs)
        super(CustomAbstractEventLoop).__init__()

        self.startup_time = datetime.now()

        self.pool: Optional[asyncpg.pool.Pool] = None
        self.http_session: Optional[aiohttp.ClientSession] = None

        self.database: Optional[Database] = None
        self.network: Optional[Network] = None

    async def get_context(self, message, *, cls=CustomContext):
        """Creating a custom context so new methods can be made for quality of life changes."""
        return await super().get_context(message, cls=cls)

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

        self.database = Database(self.pool)

        self.network = Network(self.http_session)

        await super().login(*args, **kwargs)

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.pool.close(), self.http_session.close()}, loop=self.loop, timeout=30.0)

        log.trace("Finished closing task(s).")

        return await super().logout()
