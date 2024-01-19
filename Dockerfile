FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN apt-get update && apt-get install -y default-mysql-client
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . /app/