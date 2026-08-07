FROM ghcr.io/astral-sh/uv:0.12.0 AS uv

FROM python:3.14.0-slim AS runtime

ENV PATH="/workspace/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=uv /uv /uvx /bin/

WORKDIR /workspace

COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/README.md ./apps/api/
COPY apps/api/src ./apps/api/src

RUN uv sync --frozen --no-dev --package studyhive-api

RUN addgroup --system --gid 10001 studyhive \
    && adduser --system --uid 10001 --ingroup studyhive studyhive \
    && mkdir -p /var/lib/studyhive/storage \
    && chown -R studyhive:studyhive /var/lib/studyhive

USER studyhive

EXPOSE 8000

CMD ["uvicorn", "studyhive.main:app", "--host", "0.0.0.0", "--port", "8000"]
