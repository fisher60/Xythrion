import functools
import logging
from io import BytesIO
from typing import Any, Callable, Coroutine

import numpy as np
from discord import File

from .shortcuts import DefaultEmbed

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except Exception as e:
    log.error("Error when importing Matplotlib.", exc_info=(type(e), e, e.__traceback__))


async def plot_and_save(func: Callable):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        kwargs["loop"] = self.bot.loop

        return await self.bot.loop.run_in_executor(None, func, *args, **kwargs)

    return wrapper


@plot_and_save
def graph_2d(x: np.ndarray, y: np.ndarray, **kwargs) -> DefaultEmbed:
    buffer = BytesIO()
    fig, ax = plt.subplots()
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    ax.grid(True, linestyle="-.", linewidth=0.5)

    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    ax.plot(x, y)

    fig.savefig(buffer, format="png")
    buffer.seek(0)

    file = File(fp=buffer.read(), filename="temporary_graph_file.png")

    return DefaultEmbed(kwargs["loop"], embed_attachment=file)
