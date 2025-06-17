FROM python:3.12-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Install only necessary dependencies for poetry
RUN apk add --no-cache curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Export dependencies
RUN poetry export -f requirements.txt --output requirements.txt

# Final image
FROM alpine:3.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/pyenv/bin:/opt/pyenv/shims:$PATH" \
    PYENV_ROOT="/opt/pyenv"

WORKDIR /app

# Install only the minimal required packages for building Python
# Based on pyenv's recommended build dependencies
RUN apk add --no-cache \
    # Essential build tools
    build-base \
    # Git for pyenv
    git \
    # Required for Python compilation
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    # Needed for environments
    bash

# Install pyenv with minimal footprint
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git /opt/pyenv && \
    cd /opt/pyenv && src/configure && make -C src

# Install Python versions with pyenv
RUN PYTHON_CONFIGURE_OPTS="--enable-optimizations --with-lto" \
    pyenv install -v 3.11.8 && \
    PYTHON_CONFIGURE_OPTS="--enable-optimizations --with-lto" \
    pyenv install -v 3.12.2 && \
    PYTHON_CONFIGURE_OPTS="--enable-optimizations --with-lto" \
    pyenv install -v 3.13.0a4 && \
    pyenv global 3.12.2 && \
    # Clean up cache
    rm -rf /tmp/* /var/cache/apk/*

# Install tox
RUN pip install tox

# Create a non-root user
RUN addgroup -S django && \
    adduser -S -G django django && \
    chown -R django:django /app

# Copy configuration files
COPY --from=builder /app/pyproject.toml /app/requirements.txt ./
COPY tox.ini ./

# Give access to pyenv for non-root user
RUN chmod -R 775 /opt/pyenv && \
    chown -R django:django /opt/pyenv

# Switch to non-root user
USER django

# Install project dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY --chown=django:django . .

# Default command
CMD ["/opt/pyenv/versions/3.12.2/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
