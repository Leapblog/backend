FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir /api


WORKDIR /api

COPY  poetry.lock pyproject.toml /api/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . /api/
ENTRYPOINT [ "sh", "entrypoint.sh" ]
