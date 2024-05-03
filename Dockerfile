FROM python:3.12.3-slim-bullseye as base

EXPOSE 8000
ENV PORT=8000

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

# Install necessary soft
RUN apt-get update \
    && apt-get clean

# Install uv
RUN pip install uv

# Dev environment
FROM base as dev

ENV DEVELOPMENT=1 \
    DEBUG=1

# Copy & install dependencies
COPY ./requirements ./requirements
RUN uv pip install --system -r ./requirements/dev.txt

COPY . .

CMD ["bash", "scripts/run.sh"]

# Production environment
FROM base as prod

RUN useradd -mr nonroot
ENV PATH=$PATH:/home/nonroot/.local/bin

COPY /requirements ./requirements
RUN uv pip install --system --no-cache -r ./requirements/prod.txt

COPY --chown=nonroot:nonroot . .

USER nonroot

CMD ["bash", "scripts/run.sh"]
