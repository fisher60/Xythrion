import base64
import collections
import json
import zlib
from typing import Any, Dict

from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, check_for_subcommands


class Factorio(Cog):
    """Giving information about the game of Factorio."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    async def decode_base64_gzipped_json_string(string: str) -> Dict[str, Any]:
        """
        With a string that's been encoded by base64 and compressed, this method unpacks and delivers a dictionary.

        Skipping first byte after string is converted to bytes then a bytearray to gloss over version number.

        Decompressed with gzip, then loaded by json into a dictionary with human-readable information.

        Source: https://wiki.factorio.com/Blueprint_string_format
        """
        b_array = bytearray(bytes(string, encoding="utf-8"))[1:]
        b64 = base64.b64decode(b_array)

        return json.loads(zlib.decompress(b64))

    @group()
    async def factorio(self, ctx: Context) -> None:
        """The group command for Factorio."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @factorio.command(aliases=("total",))
    async def total_items(self, ctx: Context, string: str) -> None:
        """Extracting an image out of base64 gzipped json from a string."""
        data = await self.decode_base64_gzipped_json_string(string)

        counts = collections.Counter([item["name"] for item in data["blueprint"]["entities"]])

        embed_desc_string = '\n'.join(f"**{k.replace('-', ' ').title()}:** {v}" for k, v in counts.items())

        embed_desc_string += f"\n\n**Total Items:** {sum(v for v in counts.values())}"

        embed = DefaultEmbed(ctx, desc=embed_desc_string, title="Items in blueprint:")

        await ctx.send(embed=embed)
