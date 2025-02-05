ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim AS webapp

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=/app/requirements.txt \
    python -m pip install -r /app/requirements.txt
    
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY . .

USER appuser

EXPOSE 8000

CMD ["python", "server.py"]