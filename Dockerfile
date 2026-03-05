FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    postgresql-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -path "*/tests/*" -delete && \
    find /opt/venv -path "*/test/*" -delete

FROM python:3.11-alpine AS production

RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

WORKDIR /app

RUN apk add --no-cache libpq

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=appuser:appgroup . .

RUN mkdir -p staticfiles media && \
    chown -R appuser:appgroup staticfiles media

USER appuser

ARG SECRET_KEY=build-time-dummy-key-not-used-at-runtime
ENV SECRET_KEY=$SECRET_KEY

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "library_app.wsgi:application"]
