# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# ------------------
# WORKDIR /app

# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser
# ------------------
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt 
    
RUN   
# RUN useradd -ms /bin/bash admin
# COPY app /app
WORKDIR /app
# RUN chown -R admin:admin /app
# RUN chmod 755 /app

USER root

COPY . .

EXPOSE 8000

CMD ["gunicorn", "csv_upload_backend.server:app", "--bind=0.0.0.0:8000"]

