from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

BASE_URL = "https://uwu-senpai.com/uwu-stutter"


class UWU(Cog):
    """I don't like this."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def uwu(self, ctx: Context, *, text: str) -> None:
        """Uwuifies a string, along with stutter."""
        data = await self.bot.request(f"{BASE_URL}/{text}")

        embed = DefaultEmbed(ctx, desc=data["message"])

        await ctx.send(embed=embed)
