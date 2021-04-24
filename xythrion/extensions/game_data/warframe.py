from discord.ext.commands import Cog, Context, group

from xythrion import CustomContext, Xythrion
from xythrion.utils import DefaultEmbed, and_join, check_for_subcommands

BASE_URL = "https://api.warframestat.us"
PLATFORMS = ("pc", "ps4", "xb1", "swi")
PLANET_CYCLES = ("earth", "cetus")


class Warframe(Cog):
    """Getting information about the state of Warframe."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def warframe(self, ctx: Context) -> None:
        """The group command for information on the game of Warframe."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @warframe.command()
    async def state(self, ctx: CustomContext, platform: str = "pc") -> None:
        """Getting world states from different planets."""
        if platform not in PLATFORMS:
            embed = DefaultEmbed(
                ctx, desc=f"Please pick a platform from the following: {and_join(PLATFORMS)}"
            )

            return await ctx.send(embed=embed)

        data = await self.bot.request(f"{BASE_URL}/{platform}")

        planet_cycles = "\n".join(
            f"**{planet.title()}** - {data[planet + 'Cycle']['timeLeft']} remaining"
            for planet in PLANET_CYCLES
        )

        embed = DefaultEmbed(ctx, desc=planet_cycles)

        await ctx.send(embed=embed)
