FROM python:3.11.2-slim AS compile-image
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update \
    \
    && apt install -y \
    gcc \
    libpq-dev \
    && python -m venv /opt/venv
COPY ./requirements requirements
ENV PATH="/opt/venv/bin:$PATH"
# local or production
ARG ENV=local
RUN pip install --no-cache-dir -r requirements/$ENV.txt

FROM python:3.11.2-slim AS build-image
RUN apt update \
    \
    && apt install -y \
    libpq-dev \
    && mkdir /socket \
    && groupadd -r -g 1001 app \
    && useradd -r -u 1001 -g app app \
    && chown -R app:app /socket \
    && chmod -R a+rwx /socket
VOLUME /socket

USER app
COPY --chown=app:app --from=compile-image /opt/venv /opt/venv
COPY --chown=app:app . /app
COPY --chown=app:app /config /app/config

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
