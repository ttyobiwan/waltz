from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    """Uvicorn server with custom configuration."""

    CONFIG_KWARGS = {"lifespan": "off"}
