import logging
import re

from discord.ext.commands import Cog, Context, group
from tabulate import tabulate

from xythrion.bot import Xythrion
from xythrion.constants import WeatherAPIs
from xythrion.utils import check_for_subcommands

EARTH_URL = "https://api.openweathermap.org/data/2.5/forecast?zip={0},{1}&appid={2}"
MARS_URL = f"https://api.nasa.gov/insight_weather/?api_key={WeatherAPIs.MARS}&feedtype=json&ver=1.0"

ZIP_CODE_PATTERN = re.compile(r"^\d{5}$")

log = logging.getLogger(__name__)

# https://stackoverflow.com/a/25826265/12506727


class Weather(Cog):
    """Weather for different planets."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def weather(self, ctx: Context) -> None:
        """The group command for getting weather."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @weather.command()
    async def mars(self, ctx: Context) -> None:
        """Getting weather on the planet of Mars."""
        data = await self.bot.network.request(MARS_URL)
        sol_numbers = data["sol_keys"]
        sols = {sol: [v for k, v in data[sol]["PRE"].items() if k != "ct"] for sol in sol_numbers}

        table = tabulate(
            [[sol_numbers[i]] + x for i, x in enumerate([v for v in sols.values()])],
            ["sols", *["av", "mn", "mx"]],
            showindex=False,
            numalign="left",
            stralign="right",
        )

        await ctx.send(f"```\n{table}\n```")

    @weather.command()
    async def earth(self, ctx: Context, zip_code: int) -> None:
        """Getting weather on the planet of Earth."""
        ...
