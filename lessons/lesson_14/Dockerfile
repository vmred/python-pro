FROM python:3.10-slim

ENV HOME=/home/applications/cards
ENV DB_HOST="host.docker.internal"

RUN mkdir -p $HOME

WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . $HOME
COPY .env $HOME

RUN pipenv install

EXPOSE 8000

CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 127.0.0.1:8000
