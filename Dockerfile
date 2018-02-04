FROM node:8 AS build
WORKDIR /build

COPY . /build

RUN npm i -g gulp-cli
RUN npm i

RUN gulp build


FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --three --system

COPY --from=build /build/timestrap/static /app/timestrap/static

RUN python3 manage.py collectstatic --noinput

