FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config cache-dir /tmp/poetry-cache && \
    poetry config installer.parallel true && \
    poetry install --with dev --no-root

# Copy application code
COPY . .

# Expose port for the Django dev server
EXPOSE 8080

# Run the Django development server
CMD ["poetry", "run", "example"]
