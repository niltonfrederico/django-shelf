# Python 3.11
FROM python:3.11-slim AS python-3.11
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config cache-dir /tmp/poetry-cache && \
    poetry config installer.parallel true && \
    poetry install --no-root

# Python 3.12
FROM python:3.12-slim AS python-3.12
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config cache-dir /tmp/poetry-cache && \
    poetry config installer.parallel true && \
    poetry install --no-root

# Python 3.13
FROM python:3.13-slim AS python-3.13
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config cache-dir /tmp/poetry-cache && \
    poetry config installer.parallel true && \
    poetry install --no-root

# Final image for running the application - uses 3.13 by default
FROM python-3.13 AS example

# Copy application code
COPY . .

# Expose port for the Django dev server
EXPOSE 8080

# Run the Django development server
CMD ["./example/start-example.sh"]
