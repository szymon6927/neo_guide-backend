FROM python:3.8.0-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements /requirements
RUN pip install -r /requirements/requirements.txt

WORKDIR /app
COPY . .
