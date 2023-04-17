FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3-pip python3-dev default-libmysqlclient-dev build-essential

WORKDIR /code

COPY pyproject.toml /code

RUN pip install poetry

RUN poetry install

COPY . /code

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
