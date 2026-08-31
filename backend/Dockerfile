# Build the application in the `/app` directory.

# Use the official uv image with Python 3.13 on Debian Bookworm (slim variant).
# This image includes both Python and uv pre-installed.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#available-images
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
# Disable Python downloads, because use the system interpreter If 
# using a managed Python version, it needs to be copied from the 
# build image into the final image; See `standalone.Dockerfile`

# Optional: add build arg for creation date
ARG BUILD_DATE

LABEL org.opencontainers.image.title="full-stack-fastapi-template"
LABEL org.opencontainers.image.description="Production-ready FastAPI application"
LABEL org.opencontainers.image.url="https://github.com/alex-polo/full-stack-fastapi-template"
LABEL org.opencontainers.image.source="https://github.com/alex-polo/full-stack-fastapi-template"
# LABEL org.opencontainers.image.source="https://github.com/alex-polo/full-stack-fastapi-template"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.authors="polonnikov.alexander@gmail.com"
# LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.vendor="apolo, Inc"
# LABEL org.opencontainers.image.revision

# Prevent uv from downloading Python (the base image already provides it).
ENV UV_PYTHON_DOWNLOADS=0

# Disable Python output buffering to ensure logs appear immediately 
# in container logs.
ENV PYTHONUNBUFFERED=1

# Caching
# Use 'copy' link mode to avoid hard-linking issues between cache and target filesystems.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Compiling Python source files to bytecode is typically desirable for production images
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# Use `/app` as the working directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy the entire project source into the image.
# Ensure `.venv` is excluded via `.dockerignore` to avoid platform conflicts.
COPY . /app

# Intermediate layers
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev


# Use a final image without uv
FROM python:3.14-slim-bookworm

# Install curl for health checks and remove apt lists to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/certificates && \
    chown nonroot:nonroot /app/certificates

# Use the non-root user to run our application
USER nonroot

# Use `/app` as the working directory
WORKDIR /app

RUN chmod +x ./scripts/prestart.sh

# Reset the entrypoint, don't invoke `uv`
# ENTRYPOINT ["./scripts/prestart.sh"]

# # Run the FastAPI application by production mod
# CMD ["run_main"]

# ENTRYPOINT ["./scripts/prestart.sh"]

# Run the development entrypoint defined in pyproject.toml.
#CMD ["run_main"]