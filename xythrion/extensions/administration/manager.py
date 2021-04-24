from typing import Optional

from discord.ext.commands import Cog, Context, command, is_owner

from xythrion import Xythrion
from xythrion.utils import DefaultEmbed


class Manager(Cog, command_attrs=dict(hidden=True)):
    """Changing permissions of guilds/users in different cases for usage of the bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    @is_owner()
    async def restore_guild_api_permissions(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Restores bot usage privileges for a guild."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM Blocked_Guilds WHERE guild_id = $1",
                guild_id if guild_id else ctx.guild.id,
            )

        guild = self.bot.get_guild(guild_id) if not guild_id else ctx.guild

        embed = DefaultEmbed(
            ctx,
            desc=f'Bot usage privileges restored for guild "{guild.name if guild else guild_id}".',
        )

        await ctx.send(embed=embed)

    @command()
    @is_owner()
    async def restore_user_api_permissions(self, ctx: Context, user_id: Optional[int] = None) -> None:
        """Restores bot usage privileges for a user."""
        await self.bot.db.delete(table="Blocked_Users", info={"user_id": user_id or ctx.author.id})

        user = self.bot.get_user(user_id) if user_id else ctx.author

        embed = DefaultEmbed(
            ctx,
            desc=f"Bot usage privileges restored for user {user.name if user else user_id}.",
        )

        await ctx.send(embed=embed)

    @command()
    @is_owner()
    async def remove_guild_api_permissions(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Removes bot usage privileges for a guild."""
        await self.bot.db.insert(table="Blocked_Guilds", info={"guild_id": guild_id or ctx.guild.id})

        guild = self.bot.get_guild(guild_id) if not guild_id else ctx.guild

        embed = DefaultEmbed(
            ctx,
            desc=f'Bot usage privileges removed from guild "{guild.name if guild else guild_id}".',
        )

        await ctx.send(embed=embed)

    @command()
    @is_owner()
    async def remove_user_api_permissions(self, ctx: Context, user_id: Optional[int] = None) -> None:
        """Removes bot usage privileges for a user."""
        await self.bot.db.insert(table="Blocked_Users", info={"user_id": user_id or ctx.author.id})

        user = self.bot.get_user(user_id) if user_id else ctx.author

        embed = DefaultEmbed(
            ctx,
            desc=f"Bot usage privileges Removed from user {user.name if user else user_id}.",
        )

        await ctx.send(embed=embed)
