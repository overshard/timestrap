FROM node:8 AS build
WORKDIR /build

COPY . /build

RUN npm i -g npm gulp-cli
RUN npm i
RUN npm rebuild node-sass --force

RUN gulp build:production


FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --three --system

COPY --from=build /build/client/static /app/client/static

RUN python3 manage.py collectstatic --noinput
