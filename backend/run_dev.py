import uvicorn

from src.core.config import APP_SETTINGS


def main() -> None:
    """Main function."""
    if APP_SETTINGS.UVICORN is None:
        raise ValueError("UVICORN settings must be provided for development mode.")

    uvicorn.run(
        "src.main:app",
        host=APP_SETTINGS.UVICORN.host,
        port=APP_SETTINGS.UVICORN.port,
        reload=APP_SETTINGS.UVICORN.reload,
        loop=APP_SETTINGS.UVICORN.loop,
        http=APP_SETTINGS.UVICORN.http,
        lifespan=APP_SETTINGS.UVICORN.lifespan,
        access_log=APP_SETTINGS.UVICORN.access_log,
        use_colors=APP_SETTINGS.UVICORN.use_colors,
    )


if __name__ == "__main__":
    main()
