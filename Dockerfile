# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# ---- Etapa de pruebas: docker build --target test .
FROM base AS test
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pytest.ini .
COPY src ./src
COPY tests ./tests
RUN pytest

# ---- Etapa final (la que se construye por defecto): solo el código, sin pytest
FROM base AS runtime
COPY src ./src
ENV PYTHONPATH=/app/src \
    INVENTARIO_DB=/data/inventario.db
RUN useradd --create-home --uid 1000 app \
    && mkdir /data \
    && chown app:app /data
USER app
VOLUME ["/data"]
ENTRYPOINT ["python", "-m", "inventario"]
CMD ["--help"]
