import asyncio
import logging
import re
from tempfile import TemporaryFile
from typing import Tuple, Union

import numpy as np
from discord.ext.commands import Cog, Context, group
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from xythrion import Xythrion, CustomContext
from xythrion.utils import DefaultEmbed, graph_2d, check_for_subcommands, remove_whitespace

log = logging.getLogger(__name__)

ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")

TIMEOUT_FOR_GRAPHS = 10.0


class Plotting(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def calculate(
        expression: str, symmetrical_bounds: Union[int, float] = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate y-axis values from a set of x-axis values, given a math expression."""
        symmetrical_bounds = abs(symmetrical_bounds)
        x = np.arange(-symmetrical_bounds, symmetrical_bounds, symmetrical_bounds / 50)
        expr = parse_expr(expression)
        x_symbol = Symbol("x")

        y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])

        return x, y

    # def create_graph(self, ctx: Context, graph_input: str) -> DefaultEmbed:
    #     """Creates a graph object after getting values within a domain from an expression."""
    #     with TemporaryFile(suffix=".png") as buffer:
    #         with Graph(ctx, buffer, *self.calculate(graph_input)) as embed:
    #             return embed

    @group(aliases=("graph",))
    async def plot(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @plot.command(aliases=("ex",))
    async def expression(self, ctx: CustomContext, *, expression: remove_whitespace) -> None:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if "^" in expression:
            expression = expression.replace("^", "**")

        if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
            embed = DefaultEmbed(ctx, desc=f"Illegal character in expression: {illegal_char.group(0)}")

            return await ctx.send(embed=embed)

        future = self.bot.loop.run_in_executor(None, self.create_graph, ctx, expression)

        try:
            with ctx.typing():
                embed = await asyncio.wait_for(future, TIMEOUT_FOR_GRAPHS, loop=self.bot.loop)

                await ctx.send(file=embed.file, embed=embed)

        except asyncio.TimeoutError:
            embed = DefaultEmbed(ctx, desc=f"Timed out after {TIMEOUT_FOR_GRAPHS} seconds.")

            await ctx.send(embed=embed)

    @plot.command(aliases=("point",), enabled=False)
    async def points(self, ctx: CustomContext, *, points: remove_whitespace) -> None:
        """
        plots points on a plot.

        Format: (x0, y0), (x1, y1), (x2, y2),... up to 10 points.
        """
        if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
            embed = DefaultEmbed(ctx, desc="Illegal character(s) in point array.")

            return await ctx.send(embed=embed)

        # *_ catches any other dimension of the array, so only 2d is captured.
        x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

        # embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

        embed = await graph_2d(x, y)

        await ctx.send(file=embed.file, embed=embed)
