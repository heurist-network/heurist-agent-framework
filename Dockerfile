FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Capture git commit hash at build time
ARG GITHUB_SHA=unknown
ENV GITHUB_SHA=${GITHUB_SHA}

# Copy mesh project files for dependency installation for better caching
COPY mesh/pyproject.toml mesh/uv.lock ./mesh/

# Install supervisor for process management, curl for healthchecks, git for dependency installation, libpq-dev and gcc for psycopg2
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' >/etc/apt/apt.conf.d/keep-cache && \
    apt-get update && \
    apt-get install -yqq --no-install-recommends \
    supervisor \
    curl \
    git \
    libpq-dev \
    gcc \
    libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Add supervisor configuration
COPY mesh/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    cd mesh && \
    uv sync --frozen --no-install-project --no-dev

# Add the rest of the project source code
COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/app/mesh/.venv/bin:$PATH"

# Run requirements check to verify all dependencies are installed correctly
RUN cd mesh && python requirements_checker.py && echo "Requirements check passed!" || (echo "Requirements check failed!" && exit 1)

# Reset the entrypoint
ENTRYPOINT []

# Run supervisor as the main process
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
