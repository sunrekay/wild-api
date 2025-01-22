FROM python:3.11 AS python-base

RUN apt-get update && \
    apt-get install -y cron

RUN mkdir app

WORKDIR  /app

COPY /pyproject.toml /app
COPY /poetry.lock /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN mkdir certs
RUN openssl genrsa -out certs/jwt-private.pem 2048
RUN openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

CMD python3 src/events.py && gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8001