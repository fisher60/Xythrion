from xythrion import Xythrion
from xythrion.extensions.requesters.cats import Cats
from xythrion.extensions.requesters.reddit import Reddit
from xythrion.extensions.requesters.tinyy import Tinyy
from xythrion.extensions.requesters.uwu import UWU
from xythrion.extensions.requesters.weather import Weather


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Cats(bot))
    bot.add_cog(Reddit(bot))
    bot.add_cog(Weather(bot))
    bot.add_cog(UWU(bot))
    bot.add_cog(Tinyy(bot))
