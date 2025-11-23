FROM ghcr.io/astral-sh/uv:latest AS uv

FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.13-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --system

FROM --platform=linux/amd64 public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 AS adapter

FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.13-slim AS development

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY ./agent /app/agent

ENV PORT=8080

CMD ["python", "-m", "uvicorn", "agent.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

FROM development AS production

COPY --from=adapter /lambda-adapter /opt/extensions/lambda-adapter

CMD ["python", "-m", "agent.app"]
