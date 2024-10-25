FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .


ENTRYPOINT ["/entrypoint.sh"]