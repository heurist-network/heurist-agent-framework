FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:5c8edeb8b5644b618882e06ddaa8ddf509dcd1aa7d08fedac7155106116a9a9e

# Capture git commit hash at build time
ARG GITHUB_SHA=unknown
ENV GITHUB_SHA=${GITHUB_SHA}

# Configure environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/mesh/.venv/bin:$PATH"

# Install curl for healthchecks, git for dependency installation, libpq-dev and gcc for psycopg2
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -yqq --no-install-recommends \
    curl \
    git \
    libpq-dev \
    gcc \
    libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy mesh project files for dependency installation for better caching
COPY mesh/pyproject.toml mesh/uv.lock ./mesh/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    cd mesh && \
    uv sync --frozen --no-install-project --no-dev

# Copy entrypoint script
COPY .docker/entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application code
COPY . .

# Run requirements check to verify all dependencies are installed correctly
# Copied after the rest of the application code as it uses it to verify dependencies
RUN python /app/.docker/requirements_checker.py && echo "Requirements check passed!" || (echo "Requirements check failed!" && exit 1)

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
