from xythrion.bot import Xythrion
from xythrion.extensions.game_data.factorio import Factorio


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Factorio(bot))
