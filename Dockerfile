# Obtaining Python.
FROM python:3.9-slim

# Allow service to handle stops gracefully.
STOPSIGNAL SIGQUIT

# Set pip to have cleaner logs and no saved cache.
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Installing poetry
RUN pip install --user poetry

# Adding poetry to the PATH environment variable.
ENV PATH="${PATH}:/root/.local/bin"

# Create the working directory.
WORKDIR /xythrion

# Copy configuration files.
COPY pyproject.toml poetry.lock /xythrion/

# Install packages without development packages.
RUN poetry install --no-dev --no-interaction --no-ansi

# Set SHA build argument.
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Copy working directory.
COPY . .

# Run the bot.
CMD ["python", "-m", "xythrion"]
