<p align="center">
    <img src="/images/icon.jpg" alt=""/>
</p>
<h1 align="center">Xythrion v2.0</h1>
<h3 align="center">Graphing manipulated data through discord.py</h3>
<p align="center">
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a> -
    <a href="#development">Development</a> -
    <a href="#changelog">Changelog</a>
</p>

# Setup:

*NOTE*: The following assumes that you've copied and modified the contents of `.env-example` to `.env`.

1. Setting up the database:

```shell
docker pull postgres
docker run --name postgres -e POSTGRES_PASSWORD=placeholder -d postgres
```

2. Starting the bot:
   The entire bot can be set up with `docker-compose up`.

# Development:

- When dependencies are updated, run `poetry lock`.
- When linting code, do `poetry run task lint` after running `poetry run task precommit` a total of 1 time ever.
