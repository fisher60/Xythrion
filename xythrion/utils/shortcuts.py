import typing as t
from datetime import datetime

from discord import Embed
from discord.ext.commands import Context
from humanize import naturaldelta

from xythrion import Xythrion


def markdown_link(s: str, link: str) -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    return f"[`{s}`]({link})"


def and_join(items: t.Union[list, tuple], sep: str = ", ") -> str:
    """Joins a list by a separator with an 'and' at the very end for readability."""
    return f"{sep.join(str(x) for x in items[:-1])}{sep}and {items[-1]}"


async def check_for_subcommands(ctx: Context) -> None:
    """If an invalid subcommand is passed, this is brought up."""
    lst = ", ".join([x.name for x in ctx.command.commands if x.enabled])

    error_string = f"Unknown command. Available group command(s): {lst}"

    embed = DefaultEmbed(ctx, description=error_string)

    await ctx.send(embed=embed)


class DefaultEmbed(Embed):
    """Subclassing the embed class to set defaults."""

    def __init__(self, ctx: t.Union[Context, Xythrion], **kwargs) -> None:
        super().__init__(**kwargs)

        startup_time = ctx.bot.startup_time if isinstance(ctx, Context) else ctx.startup_time

        self.set_footer(text=f"Bot uptime: {naturaldelta(datetime.now() - startup_time)}.")

        if "embed_attachment" in kwargs.keys():
            self.file = kwargs["embed_attachment"]

            self.set_image(url="attachment://temporary_graph_file.png")

        elif "description" in kwargs.keys() or "desc" in kwargs.keys():
            self.description = kwargs["description"] if "description" in kwargs.keys() else kwargs["desc"]

            if "`" not in self.description and "\n" not in self.description:
                self.description = f"`{self.description}`"
