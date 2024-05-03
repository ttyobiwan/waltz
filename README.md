# waltz

Quick boilerplate for Django.

## Installation

Install Python via tool like pyenv or rye. Then, install uv.

Create a new virtual environment using uv:

```bash
uv venv
```

Install all dependencies:

```bash
uv sync pip install -r requirements/dev.txt
```

Setup .env file:

```
# Django
DJANGO_SETTINGS_MODULE=src.config.settings.dev
# Postgres
POSTGRES_DB=waltz
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
```

## Batteries

- Logging
- Celery
- Redis cache
