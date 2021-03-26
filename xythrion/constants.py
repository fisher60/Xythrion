from os import environ
from typing import NamedTuple

__all__ = ("Config", "Postgresql", "WeatherAPIs")


class Config(NamedTuple):
    TOKEN = environ.get("BOT_TOKEN")
    GITHUB_URL = environ.get("GITHUB_URL", "https://github.com/Xithrius/Xythrion")


class Postgresql(NamedTuple):
    USER = environ.get("POSTGRES_USER")
    PASSWORD = environ.get("POSTGRES_PASSWORD")
    HOST = environ.get("POSTGRES_HOST")
    DATABASE = environ.get("POSTGRES_DB")

    asyncpg_config_url = f"postgres://{USER}@{HOST}:5432/{DATABASE}"
    asyncpg_config = {"user": USER, "password": PASSWORD, "host": HOST, "db": DATABASE}


class WeatherAPIs(NamedTuple):
    EARTH = environ.get("OPENWEATHERMAP_TOKEN")
    MARS = environ.get("NASA_TOKEN")
