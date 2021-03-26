from os import environ
from typing import NamedTuple

__all__ = ("Config", "Postgresql", "WeatherAPIs")


class Config(NamedTuple):
    TOKEN = environ.get("BOT_TOKEN")
    GITHUB_URL = environ.get("GITHUB_URL", "https://github.com/Xithrius/Xythrion")


class Postgresql(NamedTuple):
    USER = environ.get("POSTGRES_USER")
    HOST = environ.get("POSTGRES_HOST")
    DATABASE = environ.get("POSTGRES_DATABASE")

    asyncpg_config_url = f"postgres://{USER}@{HOST}:5432/{DATABASE}"


class WeatherAPIs(NamedTuple):
    EARTH = environ.get("OPENWEATHERMAP_TOKEN")
    MARS = environ.get("NASA_TOKEN")
