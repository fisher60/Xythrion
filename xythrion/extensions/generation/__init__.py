from xythrion.bot import Xythrion
from xythrion.extensions.generation.graphing import Graphing
from xythrion.extensions.generation.randoms import Randoms
from xythrion.extensions.generation.vectorization import Vectorization


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Graphing(bot))
    bot.add_cog(Randoms(bot))
    bot.add_cog(Vectorization(bot))
