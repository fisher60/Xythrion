from discord import Message
from discord.ext.commands import Cog

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, markdown_link


class Reddit(Cog):
    """Gives information about posts from Reddit."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Scans for Reddit posts and provides information on them."""
        if "https://www.reddit.com/r/" in message.content:
            url = f'{message.content.rsplit("/", maxsplit=1)[0]}.json'

            data = await self.bot.request(url)

            d = data[0]["data"]["children"][0]["data"]

            # I don't want this bot to have anything to do with anything not SFW.
            if d["over_18"]:
                return

            d = {
                "Title": d["title"],
                "Subreddit": markdown_link(d["subreddit"], f'https://www.reddit.com/r/{d["subreddit"]}'),
                "Upvotes": d["ups"],
                "Upvotes/downvotes": f'{d["upvote_ratio"] * 100}%',
                "Image url": markdown_link("Link", d["url"]),
            }

            formatted = "\n".join(f"**{k}**: {v}" for k, v in d.items())

            embed = DefaultEmbed(self.bot, description=formatted)

            await message.channel.send(embed=embed)
