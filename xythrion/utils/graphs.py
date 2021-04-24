import asyncio
import functools
import logging
from io import BytesIO
from typing import Any, Callable

import numpy as np

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as error:
    log.error("Error when importing Matplotlib.", exc_info=(type(error), error, error.__traceback__))


async def plot_and_save(func: Callable) -> Any:
    """Executor wrapper for different synchronous functions."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        return await asyncio.get_event_loop().run_in_executor(func, *args, **kwargs)

    return wrapper


@plot_and_save
def graph_2d(x_points: np.ndarray, y_points: np.ndarray) -> BytesIO:
    """Graphing points and saving said graph to a file."""
    buffer = BytesIO()
    fig, axis = plt.subplots()

    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    axis.grid(True, linestyle="-.", linewidth=0.5)

    axis.spines["left"].set_position("zero")
    axis.spines["right"].set_color("none")
    axis.spines["bottom"].set_position("zero")
    axis.spines["top"].set_color("none")

    axis.plot(x_points, y_points)

    fig.savefig(buffer, format="png")

    return buffer
