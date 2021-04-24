import re

from discord.ext.commands import Cog, command

from xythrion.bot import CustomContext, Xythrion
from xythrion.utils import DefaultEmbed

BASE_URL = "https://http.cat"

ALLOWED_CODES = re.compile(r"^[0-9]{3}$")


class Cats(Cog):
    """Getting all the cats."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def http_cat(self, ctx: CustomContext, code: str) -> None:
        """Cats!"""
        if (code := re.search(ALLOWED_CODES, code)) is None:
            embed = DefaultEmbed(ctx, desc="The code should only be 3 integers.")

            return await ctx.send(embed=embed)

        embed = DefaultEmbed(ctx, image_url=f"{BASE_URL}/{code.group(0)}")

        await ctx.send(embed=embed)
