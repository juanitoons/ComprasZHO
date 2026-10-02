FROM python:3.11 AS builder

ARG RAILWAY_PUBLIC_DOMAIN

ENV NEXT_TELEMETRY_DISABLED=1
ENV NPM_CONFIG_UPDATE_NOTIFIER=false
ENV NPM_CONFIG_FUND=false
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/.venv

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY rxconfig.py ./

RUN reflex init

COPY . ./

RUN reflex export --loglevel debug --frontend-only --no-zip

FROM caddy:2.11 AS caddy

COPY Caddyfile /etc/caddy/Caddyfile

RUN caddy fmt --overwrite /etc/caddy/Caddyfile

FROM python:3.11

ARG RAILWAY_PUBLIC_DOMAIN

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app /app

COPY --from=caddy /etc/caddy/Caddyfile /etc/caddy/Caddyfile
COPY --from=caddy /usr/bin/caddy /usr/bin/caddy

COPY --from=harnesscommunity/base /usr/bin/parallel /usr/bin/parallel

CMD parallel --ungroup --halt now,fail=1 ::: \
    "reflex run --backend-only --env prod" \
    "caddy run --config /etc/caddy/Caddyfile 2>&1"